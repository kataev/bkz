# -*- coding: utf-8 -*-
from datetime import date
from django.db.models import Sum

from whs.brick.models import Brick
from whs.bill.models import *
from whs.manufacture.models import *

def bricks(request):
    Bricks = Brick.objects.all()

    date = date.today().replace(day=1)
    sold = Sold.objects.filter(doc__date__gte=date).values('brick').annotate(s=Sum('amount'))
    add = Add.objects.filter(doc__date__gte=date).values('brick').annotate(s=Sum('amount'))
    t_from = Transfer.objects.filter(doc__date__gte=date).values('brick').annotate(s=Sum('amount'))
    t_to = Transfer.objects.filter(doc__date__gte=date,bill_sold_related__isnull=False).values('brick').annotate(s=Sum('amount'))

    sold = dict(map(lambda x: [x['brick'],x['s']],sold))
    add = dict(map(lambda x: [x['brick'],x['s']],add))
    t_from = dict(map(lambda x: [x['brick'],x['s']],t_from))
    t_to = dict(map(lambda x: [x['brick'],x['s']],t_to))
    for b in Bricks:
        b.sold = sold.get(b.pk,0)
        b.add = add.get(b.pk,0)
        b.t_from = t_from.get(b.pk,0)
        b.t_to = t_to.get(b.pk,0)
        b.begin = b.total + b.sold + b.t_from - b.t_to - b.add

        print b._sold

    return dict(Bricks=Bricks)