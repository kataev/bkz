# -*- coding: utf-8 -*-
import datetime
from itertools import groupby

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from bkz.make.models import Forming,Warren
from bkz.make.forms import FormingFactory, WarrenFactory,WarrenTTSFactory,WidthColorForm
from bkz.whs.forms import DateForm,YearMonthFilter


def index(request):
    datefilter = YearMonthFilter(request.GET or None,model=Forming)
    queryset = Forming.objects.prefetch_related('bar','raw','half')
    if datefilter.is_valid():
        data = dict(filter(lambda i:i[1],datefilter.cleaned_data.items()))
        queryset = queryset.filter(**data)
    object_list = tuple([(d, list(forming)) for d,forming in groupby(queryset, key = lambda f: f.date)])
    return render(request,'make/index.html',{'datefilter':datefilter,'object_list':object_list})


def forming(request):
    dateform = DateForm(request.GET or None)
    if dateform.is_valid():
        date = dateform.cleaned_data.get('date',datetime.date.today())
    else:
        date = datetime.date.today()
    filter = {'date':date}
    queryset = Forming.objects.filter(**filter).order_by().prefetch_related('bar','raw','half')
    order = max(tuple(f.order for f in queryset) or (1,))
    initial= [{'date':date,'order':i} for i in range(order,FormingFactory.extra+order+1)]
    factory = FormingFactory(request.POST or None,initial=initial,queryset=queryset,prefix='forming')
    instance = queryset[0] if len(queryset) > 0 else None
    widthcolor = WidthColorForm(request.POST or None,instance=instance)
    if request.method == 'POST' and factory.is_valid() and widthcolor.is_valid():
        factory.save()
        Forming.objects.filter(date=date).update(**widthcolor.cleaned_data)
        messages.success(request,'Формовка сохранена')
        return redirect(reverse('make:forming')+'?date=%s' % date.isoformat())
    return render(request,'make/forming.html',{'factory':factory,'date':date,'dateform':dateform,'widthcolor':widthcolor})


def warren(request):
    dateform = DateForm(request.GET or None)
    if dateform.is_valid():
        date = dateform.cleaned_data.get('date',datetime.date.today())
    else:
        date = datetime.date.today()
    queryset = Warren.objects.filter(source__isnull=True).filter(date=date).prefetch_related('consumer')
    order = max(tuple(f.order for f in queryset) or (1,))
    initial= [{'date':date,'order':i} for i in range(order,WarrenFactory.extra+order+1)]
    tto = WarrenFactory(request.POST or None, queryset=queryset,initial=initial,prefix='tto')
    for form in tto:
        instance=form.instance or None
        queryset = instance.consumer.all()
        order = max(tuple(f.order for f in queryset) or (1,))
        initial= [{'date':date,'order':i} for i in range(order,WarrenTTSFactory.extra+order+1)]
        form.tts = WarrenTTSFactory(request.POST or None, instance=instance,prefix=form.prefix+'-tts',initial=initial)
    if request.method == 'POST' and tto.is_valid() and all(form.tts.is_valid() for form in tto):
        print 'valid'
        tto.save()
        tts = tuple(form.tts.save() for form in tto)
        print tts
        messages.success(request,'Садка сохранена')
        return redirect(reverse('make:warren')+'?date=%s' % date.isoformat())
    for form in tto:
        for form in form.tts:
            print form.prefix
            for k,v in form.data.items():
                if form.prefix in k and not form.is_valid():
                    print '\t',k,v
    else:
        print tto.errors,tuple(form.tts.errors for form in tto)
    return render(request,'make/warren.html',dict(factory=tto,date=date,dateform=dateform))

