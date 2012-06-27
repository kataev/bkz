# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404,redirect
from django.core.urlresolvers import reverse

from whs.it.models import *
from django.db.models import F,Count,Sum

def main(request):
    """ Главная страница """
    d = Device.objects.filter(type__isnull=False).filter(type__name=u'Принтеры').order_by('type')
    w = Work.objects.all()[:40]
    c = Buy.objects.all()[:40]

    totals = Buy.objects.values('cartridge').annotate(c=Count('plug'),s=Sum('amount')).filter(s__gt=F('c')).values('cartridge__name','c','s')
    totals = map(lambda t: dict(name=t['cartridge__name'],amount=t['s']-t['c']) ,totals)

    return render(request, 'it.html',dict(divices=d,works=w,cons=c,totals=totals))



