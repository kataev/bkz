# -*- coding: utf-8 -*-
from django.db.models import Sum

from whs.bill.models import *
from whs.manufacture.models import *

def bricks(request):
    Bricks = Brick.objects.all()
    total = {}
    if request.path == '/':
        sold = dict(Sold.current.values_list('brick').annotate(Sum('amount')))
        add = dict(Add.current.values_list('brick').annotate(Sum('amount')))
        t_from = dict(Transfer.current.values_list('brick_from').annotate(Sum('amount')))
        t_to = dict(Transfer.current.values_list('brick_to').annotate(Sum('amount')))

        m_from = dict(Sorting.current.values_list('brick').annotate(Sum('amount')))
        m_to = dict(Sorted.current.values_list('brick').annotate(Sum('amount')))
        m_rmv = dict(Removed.current.values_list('brick').annotate(Sum('amount')))

        inv = dict(Write_off.current.values_list('brick').annotate(Sum('amount')))

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
                       + b.m_from + b.m_rmv - b.m_to # Перебор кирпича в цехе
                )

        for f in ['sold', 'add', 't_from', 't_to', 'total', 'begin']:
            total[f] = sum([getattr(b, f) for b in Bricks])

    return dict(Bricks=Bricks, totals=total)


