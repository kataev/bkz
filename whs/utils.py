from django.db.models import Sum
from whs.models import Sorting, Add, Sold, Write_off

def operations(filter):
    m_from = Sorting.objects.filter(brick_from__isnull=False)#.filter(**filter)
    m_to = Sorting.objects.filter(brick_from__isnull=True)#.filter(**filter)
    m_rmv = Sorting.objects.filter(brick__isnull=True)#.filter(**filter)
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