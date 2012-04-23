# -*- coding: utf-8 -*-
import datetime
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from brick.models import Brick
from manufacture.models import Add, Sorting, Sorted, Removed, Write_off
from sale.models import Sold
from whs.brick.models import make_css,make_label

def flat_form(request,Form,id):
    """ Форма  """
#    id = args[0]
    if id: instance = get_object_or_404(Form._meta.model,pk=id)
    else: instance = None
    if request.method == 'POST':
        form = Form(request.POST,instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.label = make_label(instance)
            instance.css = make_css(instance)
            instance.save()
            return redirect(instance.get_absolute_url())
    else:
        form = Form(instance=instance)
    return render(request, 'flat-form.html',dict(form=form,success=request.GET.get('success',False)))


def main(request, date=None):
    """ Главная страница """
    Bricks = Brick.objects.all()
    total = {}
    if date is None:
        date = datetime.date.today().replace(day=1)


    add = dict(Add.objects.filter(doc__date__gte=date).values_list('brick').annotate(Sum('amount')))
    sold = dict(Sold.objects.filter(doc__date__gte=date).values_list('brick').annotate(Sum('amount')))
    t_from = dict(Sold.objects.filter(doc__date__gte=date,brick_from__isnull=False).values_list('brick_from').annotate(Sum('amount')))
    t_to = dict(Sold.objects.filter(doc__date__gte=date,brick_from__isnull=False).values_list('brick').annotate(Sum('amount')))

    m_from = dict(Sorting.objects.filter(date__gte=date).values_list('brick').annotate(Sum('amount')))
    m_to = dict(Sorted.objects.filter(date__gte=date).values_list('brick').annotate(Sum('amount')))
    m_rmv = dict(Removed.objects.filter(date__gte=date).values_list('brick').annotate(Sum('amount')))

    inv = dict(Write_off.objects.filter(doc__date__gte=date).values_list('brick').annotate(Sum('amount')))

    for b in Bricks:
        b.sold = sold.get(b.pk, 0)
        b.add = add.get(b.pk, 0)
        b.t_from = t_from.get(b.pk, 0)
        b.t_to = t_to.get(b.pk, 0)
        b.sold += t_to.get(b.pk, 0)
        b.m_from = m_from.get(b.pk, 0)
        b.m_to = m_to.get(b.pk, 0)
        b.m_rmv = m_rmv.get(b.pk, 0)
        b.inv = inv.get(b.pk, 0)

        b.begin = (b.total
                   + b.sold + b.t_from - b.t_to # Накладные
                   - b.add # Приход
                   + b.inv # Инвенторизация
                   + b.m_from - b.m_to # + b.m_rmv # Перебор кирпича в цехе
            )

        b.opers = b.sold + b.add + b.t_from + b.t_to + b.m_from + b.m_to + b.m_rmv + b.inv
    for f in Brick.order:
        total[f] = sum([getattr(b, f) for b in Bricks])
    return render(request, 'main.html',dict(Bricks=Bricks, totals=total))