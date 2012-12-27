# -*- coding: utf-8 -*-
from collections import Counter
import csv
import datetime
import logging

from exceptions import ValueError
from dateutil.relativedelta import relativedelta

from django.db.models import Max, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import UpdateView, CreateView, ListView

from bkz.whs.forms import BillFilter, YearMonthFilter

from whs.forms import DateForm, VerificationForm, AgentForm, AgentCreateOrSelectForm
from whs.forms import SoldFactory, PalletFactory
from whs.models import *
from lab.models import Batch
from lab.forms import BatchFilter


from whs.utils import operations, calc

logger = logging.getLogger(__name__)

__author__ = 'bteam'

class BillSlugMixin(object):
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get('pk', None)
        year = self.kwargs.get('year', None)
        number = self.kwargs.get('number', None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        elif year is not None and number is not None:
            queryset = queryset.filter(date__year=year, number=number)

        # If none of those are defined, it's an error.
        else:
            raise AttributeError(u"Generic detail view %s must be called with "
                                 u"either an object pk or a slug."
            % self.__class__.__name__)

        try:
            obj = queryset.get()
        except self.model.DoesNotExist:
            raise Http404(_(u"No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class BillUpdateView(UpdateView):
    opers = [SoldFactory, PalletFactory]

    def form_valid(self, form):
        instance = form.save()
        context = self.get_context_data()
        opers = context.get('opers',{})

        for k,factory in opers.iteritems():
            if factory.is_valid():
                factory.save()
        if all([f.is_valid() for k,f in opers.items()]):
            return redirect(self.get_success_url())
        return self.render_to_response(dict(form=form, opers=opers))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['opers']={}
        for factory in self.opers:
            prefix = factory.get_default_prefix()
            context['opers'][prefix] = factory(self.request.POST or None, instance=self.object)
        return context

class SortingCreateView(CreateView):
    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = self.initial.copy()
        part = self.request.GET.get('part',None)
        if part:
            initial['part']=part
        return initial


#class SortingUpdateView(BillUpdateView):
#    opers = [SortedFactory]


class BillCreateView(CreateView):
    def get_initial(self):
        initial = self.initial.copy()
        if self.request.method == 'GET':
            number = self.model.objects.filter(date__year=datetime.date.today().year).aggregate(number=Max('number'))
            initial['number'] = (number.get('number') or 0) + 1
            agent = self.request.GET.get('agent', None)
            if agent:
                initial['agent'] = agent
        return initial

def bill_pk_redirect(request, pk):
    b = get_object_or_404(Bill, pk=pk)
    return redirect(b.get_absolute_url())

from django.core.exceptions import ValidationError
class BrickCreateView(CreateView):
    model = Brick

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.label = make_label(self.object)
        if Brick.objects.exclude(pk=self.object.pk).filter(label=self.object.label):
            raise ValidationError(u'Такой кирпич вроде уже есть с УИД %d!' % self.object.pk)
        self.object.css = make_css(self.object)
        self.object.save()
        return super(CreateView, self).form_valid(form)


class BrickUpdateView(UpdateView):
    model = Brick

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.label = make_label(self.object)
        self.object.css = make_css(self.object)
        self.object.save()
        return super(UpdateView, self).form_valid(form)


class BillListView(ListView):
    
    model = Bill
    paginate_by = 20

    def get_paginate_by(self, queryset):
        try: p = int(self.request.GET.get('rpp', ''))
        except ValueError: p = self.paginate_by
        return p

def bills(request):
    queryset = Bill.objects.prefetch_related('solds', 'pallets', 'solds__brick', 'solds__brick_from', 'seller',
        'agent').select_related()
    billfilter = BillFilter(request.GET or None)
    datefilter = YearMonthFilter(request.GET or None)
    rpp = request.GET.get('rpp',20)
    if billfilter.is_valid():
        data = dict(filter(lambda i:i[1],billfilter.cleaned_data.items()))
        if data.has_key('page'):
            data.pop('page')
        if data.has_key('brick'):
            data['solds__brick'] = data.pop('brick')
        if data.has_key('rpp'):
            data.pop('rpp')
        queryset = queryset.filter(**data)
    if datefilter.is_valid():
        data = dict(filter(lambda i:i[1],datefilter.cleaned_data.items()))
        queryset = queryset.filter(**data)
    return render(request,'whs/bill_list.html',dict(filter=billfilter,datefilter=datefilter,
        object_list=queryset,rpp=rpp))


def agents(request):
    alphabet = u"АБВГДЕЁЖЗИКЛМНОПРСТФХЦЧШЩЫЮЯ"
    Agents = Agent.objects.all()
    letter = request.GET.get('b', '')
    if letter:
        Agents = Agents.filter(name__iregex=u"^%s." % letter[0])
    else:
        Agents = Agents[:20]
    return render(request, 'whs/agent_list.html', dict(Agents=Agents, alphabet=alphabet))

def journal(request):
    form = DateForm(request.GET or None)
    if form.is_valid():
        date = form.cleaned_data.get('date')
    else:
        date = datetime.date.today()
    sorting = Sorting.objects.filter(source__isnull=True).filter(date=date)
    bills = Bill.objects.filter(date=date).select_related('solds','solds__brick')
    adds = []
    return render(request, 'whs/journal.html',dict(sorting=sorting,bills=bills,adds=adds,date=date))

def batchs(request):
    queryset = Batch.objects.all()
    datefilter = YearMonthFilter(request.GET or None)
    datefilter.Meta.dates = Batch.objects.dates('date', 'month')[::-1]
    batchfilter = BatchFilter(request.GET or None)
    if batchfilter.is_valid():
        pass
    rpp = request.GET.get('rpp',20)
    if datefilter.is_valid():
        data = dict(filter(lambda i:i[1],datefilter.cleaned_data.items()))
        queryset = queryset.filter(**data)
    return render(request, 'whs/add_list.html', dict(object_list=queryset,rpp=rpp,
        datefilter=datefilter,filter=batchfilter,))

def sortings(request):
    queryset = Sorting.objects.all()
    datefilter = YearMonthFilter(request.GET or None)
    datefilter.Meta.dates = Sorting.objects.dates('date', 'month')[::-1]
    # batchfilter = BatchFilter(request.GET or None)
    # if batchfilter.is_valid():
        # pass
    rpp = request.GET.get('rpp',20)
    if datefilter.is_valid():
        data = dict(filter(lambda i:i[1],datefilter.cleaned_data.items()))
        queryset = queryset.filter(**data)
    return render(request, 'whs/sorting_list.html', dict(object_list=queryset,rpp=rpp,
        datefilter=datefilter))


def brick_main(request):
    """ Главная страница """
    Bricks = Brick.objects.all()
    form = YearMonthFilter(request.GET or None)
    if form.is_valid():
        data = dict([(k, v) for k, v in form.cleaned_data.items() if v is not None])
        if data.has_key('date__month'):
            begin = datetime.date(year=data['date__year'], month=data['date__month'], day=1)
            end = begin + relativedelta(months=1)
        else:
            begin = datetime.date(year=data['date__year'], month=1, day=1)
            end = begin + relativedelta(years=1)
        before = operations(dict(date__gte=end))
        before = calc(before)
    else:
        begin = datetime.date.today().replace(day=1)
        end = begin + relativedelta(months=1)
        before = {}
    opers = operations(dict(date__range=(begin, end - datetime.timedelta(1))))
    for b in Bricks:
        if before:
            b.total += before.get(b.pk, 0)
        b.sold = opers['sold'].get(b.pk, 0)
        b.add = opers['add'].get(b.pk, 0)
        b.t_from = opers['t_from'].get(b.pk, 0)
        b.t_to = opers['t_to'].get(b.pk, 0)
        b.m_from = opers['m_from'].get(b.pk, 0)
        b.m_to = opers['m_to'].get(b.pk, 0)
        b.m_rmv = opers['m_rmv'].get(b.pk, 0)
        b.inv = opers['inv'].get(b.pk, 0)

        b.begin = (b.total
                   + b.sold + b.t_from - b.t_to # Накладные
                   - b.add # Приход
                   + b.inv # Инвенторизация
                   + b.m_from - b.m_to # + b.m_rmv # Перебор кирпича в цехе
            )
        b.opers = b.sold or b.add or b.t_from or b.t_to or b.m_from or b.m_to or b.m_rmv or b.inv
    return render(request, 'whs/brick-list.html',
        dict(Bricks=Bricks, order=Brick.order, form=form,brick_menu = get_menu(), 
            begin=begin, end=end - datetime.timedelta(1)))


def verification(request):
    form = VerificationForm(request.POST or None, request.FILES or None)
    deriv, total, c = [], {}, {}
    if form.is_valid():
        id, f = form.cleaned_data['id'], form.cleaned_data['field']
        oborot = csv.reader(form.cleaned_data['csv'], delimiter=';')
        oborot = filter(lambda r: r and isinstance(r, list) and r[0] and r[1] and r[f], oborot)
        c = Counter([int(r[id]) for r in oborot if r[id]])
        c = [k for k, v in c.iteritems() if v > 1]
        for r in oborot:
            pk, total = r[id], int(r[f])
            b = Brick.objects.get(pk=pk)
            if b.total != total:
                deriv.append(dict(brick=b, field=total, name=r[0], deriv=b.total - total))
        total = dict(base=Brick.objects.aggregate(Sum('total'))['total__sum'], csv=sum([int(r[f]) for r in oborot]))
    return render(request, 'whs/verification.html', dict(form=form, deriv=deriv, total=total, counter=c))


from webodt.shortcuts import render_to_response
def bill_print(request, pk):
    doc = get_object_or_404(Bill.objects.select_related(), pk=pk)
    return render_to_response('webodt/torg-12.odt',{'doc':doc},format='pdf',inline=True)
