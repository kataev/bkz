# -*- coding: utf-8 -*-
from collections import Counter
import csv
import datetime
import logging

from exceptions import ValueError
from dateutil.relativedelta import relativedelta
from django.db.models import Max,Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import ugettext as _

from bkz.whs.forms import BillFilter, YearMonthFilter, BillAggregateFilter
from bkz.views import CreateView, UpdateView, DeleteView, ListView
from bkz.whs.pdf import pdf_render_to_response
from django.contrib.formtools.wizard.views import SessionWizardView
from brick.views import operations, calc
from whs.forms import DateForm, YearMonthFilter, VerificationForm
from whs.models import Agent, Bill, Add, Sorting, Sorted, Brick, Sold, Write_off

logger = logging.getLogger(__name__)

__author__ = 'bteam'


class BillWizard(SessionWizardView):
    def done(self,form_list,**kwargs):
        return redirect('/')


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


class UpdateView(BillSlugMixin, UpdateView):
    pass


class DeleteView(BillSlugMixin, DeleteView):
    pass


class CreateView(CreateView):
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            initial = Bill.objects.filter(date__year=datetime.date.today().year).aggregate(number=Max('number'))
            initial['number'] = (initial.get('number') or 0) + 1
            print context['form'].instance
            context['form'].initial = initial
        print context['form'].initial
        return context

def bill_pk_redirect(request,pk):
    b = get_object_or_404(Bill,pk=pk)
    return redirect(b.get_absolute_url())


def bill_print(request, year, number):
    doc = get_object_or_404(Bill.objects.select_related(), number=number, date__year=year)
    return pdf_render_to_response('torg-12.rml', {'doc': doc})

class BillListView(ListView):
    queryset = Bill.objects.prefetch_related('solds','pallets','solds__brick','solds__brick_from').select_related()
    template_name = 'bills.html'
    paginate_by = 20
    context_object_name = 'bills'

    def get_paginate_by(self, queryset):
        try:
            p = int(self.request.GET.get('rpp',''))
        except ValueError:
            p = self.paginate_by
        return p

    def get_queryset(self):
        form = BillFilter(self.request.GET or None)
        print form.is_valid()
        if form.is_valid():
            data = dict([(k,v) for k,v in form.cleaned_data.items() if v is not None])
            if data.has_key('page'):
                data.pop('page')
            if data.has_key('year'):
                data['date__year']=data.pop('year')
            if data.has_key('month'):
                data['date__month']=data.pop('month')
            if data.has_key('brick'):
                data['solds__brick']=data.pop('brick')
            if data.has_key('rpp'):
                data.pop('rpp')
            return self.queryset.filter(**data)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(BillListView, self).get_context_data(**kwargs)
        context['form'] = BillFilter(self.request.GET or None)
        return context

def agents(request):
    alphabet = u"АБВГДЕЁЖЗИКЛМНОПРСТФХЦЧШЩЫЮЯ"
    Agents = Agent.objects.all()
    letter = request.GET.get('b','')
    if letter:
        Agents = Agents.filter(name__iregex=u"^%s." % letter[0])
    return render(request, 'agents.html', dict(Agents=Agents,alphabet=alphabet))


def stats(request):
    form = YearMonthFilter(request.GET or None)
    return render(request, 'stats.html',dict(form=form))


def main_man(request):
    form = DateForm(request.GET or None)
    if form.is_valid():
        date = form.cleaned_data.get('date')
    else:
        date = datetime.date.today()
    man = Add.objects.select_related().filter(doc__date__year=date.year,doc__date__month=date.month)
    sorting = Sorting.objects.select_related().filter(date__year=date.year,date__month=date.month)
    opers = {}
    if len(sorting):
        for m in (Sorted,):
            name = m._meta.object_name
            for o in m.objects.select_related().filter(doc__in=sorting):
                d = opers.get(o.doc_id,{})
                a = d.get(name,[])
                a.append(o)
                d[name] = a
                opers[o.doc_id] = d

        for b in sorting:
            b.opers = opers.get(b.pk,{})
    return render(request,'jurnal.html',dict(man=man,sorting=sorting,form=form))


def brick_flat_form(request, Form, id):
    """ Форма  """
    #    id = args[0]
    if id: instance = get_object_or_404(Form._meta.model, pk=id)
    else: instance = None
    if request.method == 'POST':
        form = Form(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.label = make_label(instance)
            instance.css = make_css(instance)
            instance.save()
            return redirect(instance.get_absolute_url())
    else:
        form = Form(instance=instance)
    return render(request, 'flat-form.html', dict(form=form, success=request.GET.get('success', False)))


def brick_main(request):
    """ Главная страница """
    Bricks = Brick.objects.all()
    form = YearMonthFilter(request.GET or None)
    if form.is_valid():
        data = dict([(k,v) for k,v in form.cleaned_data.items() if v is not None])
        if data.has_key('date__month'):
            begin = datetime.date(year=data['date__year'],month=data['date__month'],day=1)
            end = begin + relativedelta(months=1)
        else:
            begin = datetime.date(year=data['date__year'],month=1,day=1)
            end = begin + relativedelta(years=1)
        before = operations(dict(date__gte=end))
        before = calc(before)
    else:
        begin = datetime.date.today().replace(day=1)
        end = begin + relativedelta(months=1)
        before = {}
    opers = operations(dict(date__range=(begin,end - datetime.timedelta(1))))
    for b in Bricks:
        if before:
            b.total+= before.get(b.pk,0)
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

    return render(request, 'main.html', dict(Bricks=Bricks, order=Brick.order,form=form,begin=begin,end=end - datetime.timedelta(1)))


def calc(opers):
    d = dict()
    for k,o in opers.items():
        for i,v in o.items():
            if k in ['sold','t_from','inv','f_from']:
                d[i]=d.get(i,0) + v
            if k in ['t_to','add','m_to']:
                d[i]=d.get(i,0) - v
    return d


def operations(filter):
    m_from = Sorting.objects.filter(**filter)
    m_to = Sorted.objects.filter(type=0).filter(**filter)
    m_rmv = Sorted.objects.filter(type=1).filter(**filter)
    filter = dict([('doc__%s' % k, v) for k, v in filter.items()])
    add = Add.objects.filter(**filter)
    sold = Sold.objects.filter(**filter)
    t_from = Sold.objects.filter(**filter).filter(brick_from__isnull=False)
    t_to = Sold.objects.filter(**filter).filter(brick_from__isnull=False)
    inv = Write_off.objects.filter(**filter)

    return dict(add=dict(add.values_list('brick__id').annotate(Sum('amount')).order_by()),
        sold=dict(sold.values_list('brick__id').annotate(Sum('amount')).order_by()),
        t_from=dict(t_from.values_list('brick_from__id').annotate(Sum('amount')).order_by()),
        t_to=dict(t_to.values_list('brick__id').annotate(Sum('amount')).order_by()),
        m_from=dict(m_from.values_list('brick__id').annotate(Sum('amount')).order_by()),
        m_to=dict(m_to.values_list('brick__id').annotate(Sum('amount')).order_by()),
        m_rmv=dict(m_rmv.values_list('brick__id').annotate(Sum('amount')).order_by()),
        inv=dict(inv.values_list('brick__id').annotate(Sum('amount')).order_by()))


def verification(request):
    form = VerificationForm(request.POST or None,request.FILES or None)
    deriv,total,c = [],{},{}
    if form.is_valid():
        id,f = form.cleaned_data['id'],form.cleaned_data['field']
        oborot = csv.reader(form.cleaned_data['csv'],delimiter=';')
        oborot = filter(lambda r:r and isinstance(r,list) and r[0] and r[1] and r[f],oborot)
        c = Counter([int(r[id]) for r in oborot if r[id]])
        c = [k for k,v in c.iteritems() if v>1]
        for r in oborot:
            pk,total =  r[id],int(r[f])
            b = Brick.objects.get(pk=pk)
            if b.total != total:
                deriv.append(dict(brick=b,field=total,name=r[0],deriv=b.total-total))
        total = dict(base=Brick.objects.aggregate(Sum('total'))['total__sum'],csv=sum([int(r[f]) for r in oborot]))
    print total,deriv,c
    return render(request,'verification.html',dict(form=form,deriv=deriv,total=total,counter=c))