# -*- coding: utf-8 -*-
from collections import Counter
import csv
import datetime
import logging

from operator import itemgetter

from exceptions import ValueError
from dateutil.relativedelta import relativedelta

from django.http import Http404
from django.contrib import messages
from django.db.models import Max, Sum, F
from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import UpdateView, CreateView, ListView

from whs.forms import DateForm, VerificationForm, AgentForm, AgentCreateOrSelectForm, BillFilter, YearMonthFilter
from whs.forms import SoldFactory, PalletFactory
from whs.models import *
from bkz.lab.models import Batch, Part
from bkz.lab.forms import BatchFilter, PartAddFormSet

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
        opers = context.get('opers', {})

        for k, factory in opers.iteritems():
            if factory.is_valid():
                factory.save()
        if all([f.is_valid() for k, f in opers.items()]):
            messages.success(self.request, u'Партия сохранена')
            return redirect(self.get_success_url())
        return self.render_to_response(dict(form=form, opers=opers))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['opers'] = {}
        for factory in self.opers:
            prefix = factory.get_default_prefix()
            context['opers'][prefix] = factory(self.request.POST or None, instance=self.object)
        return context


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
        self.object = form.save()
        self.object.label = make_label(self.object)
        if Brick.objects.exclude(pk=self.object.pk).filter(label=self.object.label):
            raise ValidationError(u'Такой кирпич вроде уже есть с УИД %d!' % self.object.pk)
        self.object.css = make_css(self.object)
        self.object.save()
        messages.success(self.request, u'Сохранено')
        return super(CreateView, self).form_valid(form)


class BrickUpdateView(UpdateView):
    model = Brick

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.label = make_label(self.object)
        self.object.css = make_css(self.object)
        self.object.save()
        messages.success(self.request, u'Сохранено')
        return super(UpdateView, self).form_valid(form)


def bills(request):
    queryset = Bill.objects.prefetch_related('solds', 'pallets', 'solds__brick', 'solds__brick_from', 'seller',
                                             'agent').select_related()
    billfilter = BillFilter(request.GET or None)
    datefilter = YearMonthFilter(request.GET or None, model=Bill)
    rpp = request.GET.get('rpp', 20)
    if billfilter.is_valid():
        data = dict(filter(itemgetter(1), billfilter.cleaned_data.items()))
        if data.has_key('page'):
            data.pop('page')
        if data.has_key('brick'):
            data['solds__brick'] = data.pop('brick')
        if data.has_key('rpp'):
            data.pop('rpp')
        queryset = queryset.filter(**data)
    if datefilter.is_valid():
        data = {k: v for k, v in datefilter.cleaned_data.items() if v}
        queryset = queryset.filter(**data)
    return render(request, 'whs/bills.html', dict(filter=billfilter, datefilter=datefilter,
                                                  object_list=queryset, rpp=rpp))


def agents(request):
    alphabet = u"АБВГДЕЁЖЗИКЛМНОПРСТФХЦЧШЩЫЮЯ"
    Agents = Agent.objects.all()
    letter = request.GET.get('b', '')
    if letter:
        Agents = Agents.filter(name__iregex=u"^%s." % letter[0])
    else:
        Agents = Agents[:20]
    return render(request, 'whs/agents.html', dict(Agents=Agents, alphabet=alphabet))


def journal(request):
    form = DateForm(request.GET or None)
    if form.is_valid():
        date = form.cleaned_data.get('date')
    else:
        date = datetime.date.today()
    sorting = Sorting.objects.filter(source__isnull=True).filter(date=date)
    bills = Bill.objects.filter(date=date).select_related('solds', 'solds__brick')
    adds = []
    return render(request, 'whs/journal.html', dict(sorting=sorting, bills=bills, adds=adds, date=date))


def batchs(request):
    queryset = Batch.objects.select_related('frost_resistance', 'width').prefetch_related('parts', 'parts__rows').all()
    datefilter = YearMonthFilter(request.GET or None, model=Batch)
    factory = PartAddFormSet(request.POST or None, queryset=Part.objects.select_related('brick', 'brick__width') \
        .prefetch_related('batch', 'rows', 'batch__frost_resistance', 'batch__width').filter(brick__isnull=True))
    if request.method == 'POST' and factory.is_valid():
        factory.save()
        messages.success(request, u'Успешно сохранено!')
        return redirect(reverse_lazy('whs:Add-list'))
    rpp = request.GET.get('rpp', 20)
    if datefilter.is_valid():
        data = dict(filter(itemgetter(1), datefilter.cleaned_data.items()))
        queryset = queryset.filter(**data)
    return render(request, 'whs/batchs.html', dict(object_list=queryset, rpp=rpp,
                                                   datefilter=datefilter, factory=factory))


def sortings(request):
    def prep1(v):
        if isinstance(v, str):
            return "'%s'" % v
        else:
            return v

    def prep2(queryset):
        query, params = queryset.query.sql_with_params()
        return query.replace('SUM(T4."amount")', 'COALESCE(SUM(T4."amount"),0)') % tuple(map(prep1, params))

    q1 = Sorting.objects.filter(type=0).annotate(Sum('sorted__amount')).exclude(sorted__amount__sum=F('amount'))
    q2 = Sorting.objects.filter(type=0).annotate(Sum('sorted__amount'))
    datefilter = YearMonthFilter(request.GET or None, model=Sorting)
    rpp = request.GET.get('rpp', 20)
    if datefilter.is_valid():
        data = {k: v for k, v in datefilter.cleaned_data.items() if v}
        queryset = q2.filter(**data)
    else:
        date = datetime.date.today()
        data = {'date__year': date.year, 'date__month': date.month}
        q2 = q2.filter(**data)
        queryset = Sorting.objects.raw("(%s) UNION (%s) ORDER BY date DESC" % tuple(map(prep2, [q1, q2])))
    return render(request, 'whs/sortings.html', dict(object_list=queryset, rpp=rpp, datefilter=datefilter))


def bricks(request):
    """ Главная страница """
    Bricks = Brick.objects.all()
    form = YearMonthFilter(request.GET or None, model=Bill)
    if form.is_valid():
        data = {k: v for k, v in datefilter.cleaned_data.items() if v is not None}
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
    return render(request, 'whs/bricks.html',
                  dict(Bricks=Bricks, order=Brick.order, form=form, brick_menu=get_menu(),
                       begin=begin, end=end - datetime.timedelta(1)))


from operator import itemgetter


def verification(request):
    form = VerificationForm(request.POST or None, request.FILES or None)
    deriv, total, c = [], {}, {}
    if form.is_valid():
        id, f = [form.cleaned_data[k] for k in ('id', 'field')]
        oborot = csv.reader(form.cleaned_data['csv'], delimiter=';')
        oborot = filter(lambda r: r and isinstance(r, list) and all(itemgetter(0, 1, f)), oborot)
        c = Counter([int(r[id]) for r in oborot if r[id]])
        c = [k for k, v in c.iteritems() if v > 1]
        for r in oborot:
            pk, total = r[id], int(r[f])
            b = Brick.objects.get(pk=pk)
            if b.total != total:
                deriv.append(dict(brick=b, field=total, name=r[0], deriv=b.total - total))
        total = dict(base=Brick.objects.aggregate(Sum('total'))['total__sum'], csv=sum([int(r[f]) for r in oborot]))
    return render(request, 'whs/verification.html', dict(form=form, deriv=deriv, total=total, counter=c))


from bkz.whs.constants import mark_c
from collections import OrderedDict


def transfers(request):
    datefilter = YearMonthFilter(request.GET or None, model=Bill)
    queryset = Sold.objects.filter(brick_from__isnull=False).values_list('brick__mark', 'brick_from__mark').annotate(
        Sum('amount'))
    if datefilter.is_valid():
        data = {'doc__' + k: v for k, v in datefilter.cleaned_data.items() if v}
    else:
        date = datetime.date.today()
        data = {'doc__date__year': date.year, 'doc__date__month': date.month}
    out = OrderedDict((mark, OrderedDict((m, 0) for m, l in mark_c)) for mark, l in mark_c)
    for mark, mark_from, amount in queryset.filter(**data):
        out[mark][mark_from] += amount
    return render(request, 'whs/transfers.html', {'data': out, 'datefilter': datefilter, 'label': dict(mark_c)})


from webodt.shortcuts import render_to_response


def bill_print(request, pk):
    docs = [get_object_or_404(Bill.objects.select_related(), pk=pk)]
    if docs[0].seller_id != 1:
        doc = get_object_or_404(Bill.objects.select_related(), pk=pk)
        doc.agent = doc.seller.agent
        doc.seller = doc.bkz
        docs.append(doc)
    return render_to_response('webodt/torg-12.odt', {'docs': docs}, format='pdf', inline=True)
