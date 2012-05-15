# -*- coding: utf-8 -*-
import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from brick.models import Brick
from man.models import Add, Sorting, Sorted, Write_off
from sale.models import Sold
from sale.forms import YearMonthFilter
from whs.brick.models import make_css, make_label

def flat_form(request, Form, id):
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


def operations(filter):
    m_from = Sorting.objects.filter(**filter)
    m_to = Sorted.objectsf.filter(type=0).filter(**filter)
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

def calc(opers):
    d = dict()
    for k,o in opers.items():
        for i,v in o.items():
            if k in ['sold','t_from','inv','f_from']:
                d[i]=d.get(i,0) + v
            if k in ['t_to','add','m_to']:
                d[i]=d.get(i,0) - v
    return d


def main(request):
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