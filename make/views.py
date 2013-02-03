# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from bkz.make.models import Forming,Warren
from bkz.make.forms import FormingFactory, WarrenFactory,WarrenTTOFactory
from bkz.whs.forms import DateForm


def index(request):
    dateform = DateForm(request.GET or None)
    if dateform.is_valid():
        date = dateform.cleaned_data.get('date',datetime.date.today())
    else:
        date = datetime.date.today()
    filter = {'date':date}
    initial={'date':date}
    queryset = Forming.objects.filter(**filter).order_by().prefetch_related('bar','raw','half')
    factory = FormingFactory(request.POST or None,initial=[initial,]*FormingFactory.extra,queryset=queryset,prefix='warren')
    if request.method == 'POST' and factory.is_valid():
        factory.save()
        messages.success(request,'Формовка сохранена')
        return redirect(reverse('make:index')+'?date=%s' % date.isoformat())
    return render(request,'make/index.html',{'factory':factory,'date':date,'dateform':dateform})




def warren(request):
    dateform = DateForm(request.GET or None)
    if dateform.is_valid():
        date = dateform.cleaned_data.get('date',datetime.date.today())
    else:
        date = datetime.date.today()
    queryset = Warren.objects.filter(source__isnull=True).filter(date=date)
    initial=[{'date':date},]
    tto = WarrenFactory(request.POST or None, queryset=queryset,initial=initial)
    for form in tto:
        instance=form.instance or None
        form.tts = WarrenTTOFactory(request.POST or None, instance=instance,prefix=form.prefix+'-tts',initial=initial*WarrenTTOFactory.extra)
    if request.method == 'POST' and tto.is_valid() and all(form.tts.is_valid() for form in tto):
        tto.save()
        (form.tts.save() for form in tto)
        messages.success(request,'Садка сохранена')
        return redirect(reverse('make:warren')+'?date=%s' % date.isoformat())
    return render(request,'make/warren.html',dict(factory=tto,date=date,dateform=dateform))
        # for form in factory:
        #     if not form.factory.is_valid():
        #         for form in form.factory:
        #             print form.prefix
        #             for k,v in form.data.items():
        #                 if form.prefix in k and not form.is_valid():
        #                     print '\t',k,v
