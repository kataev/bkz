# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404,redirect

from bkz.it.models import *
from django.db.models import F,Count,Sum

def main(request):
    """ Главная страница """
    d = Device.objects.filter(type__isnull=False)
    w = Work.objects.all()[:10]
    c = Buy.objects.all()[:10]
    replaces = Plug.objects.order_by('-date').all()[:10]

    buy = dict(Buy.objects.values_list('cartridge_id').order_by().annotate(Sum('amount')))
    plug = dict(Plug.objects.values_list('bill__cartridge').order_by().annotate(Count('id')))

    totals = dict([(pk,v-plug.get(pk,0)) for pk,v in buy.items()])

    return render(request, 'it/it.html',dict(divices=d,works=w,cons=c,totals=totals,replaces=replaces))