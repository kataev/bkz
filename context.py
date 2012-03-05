# -*- coding: utf-8 -*-
import datetime
from django.db.models import Sum, Q

from whs.brick.models import Brick
from whs.bill.models import *
from whs.manufacture.models import *

def bricks(request):
    Bricks = Brick.objects.all()
    total = {}
    if request.path == '/':
        date = datetime.date.today().replace(day=1)
        sold = dict(Sold.objects.filter(doc__date__gte=date).values_list('brick').annotate(Sum('amount')))
        add = dict(Add.objects.filter(doc__date__gte=date).values_list('brick').annotate(Sum('amount')))
        t_from = dict(Transfer.objects.filter(doc__date__gte=date).values_list('brick_from').annotate(Sum('amount')))
        t_to = dict(Transfer.objects.filter(doc__date__gte=date).values_list('brick_to').annotate(Sum('amount')))

        for b in Bricks:
            b.sold = sold.get(b.pk,0)
            b.add = add.get(b.pk,0)
            b.t_from = t_from.get(b.pk,0)
            b.t_to = t_to.get(b.pk,0)
            b.sold += t_to.get(b.pk,0)
            b.begin = b.total + b.sold + b.t_from - b.t_to - b.add


        for f in ['sold','add','t_from','t_to','total','begin']:
            total[f]=sum([getattr(b,f) for b in Bricks])

    return dict(Bricks=Bricks, totals=total)