# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from bkz.make.models import Forming,Warren
from bkz.make.forms import FormingFactory, WarrenFactory
from bkz.whs.forms import DateForm


def index(request):
    dateform = DateForm(request.GET or None)
    if dateform.is_valid():
        date = dateform.cleaned_data.get('date',datetime.date.today())
    else:
        date = datetime.date.today()
    filter = {'date':date}
    initial={'date':date}
    factory = FormingFactory(request.POST or None,initial=[initial,]*FormingFactory.extra,queryset=Forming.objects.filter(**filter),prefix='warren')
    if request.method == 'POST' and factory.is_valid():
        factory.save()
        return redirect(reverse('make:index')+'?date=%s' % date.isoformat())
    return render(request,'make/index.html',{'factory':factory,'date':date,'dateform':dateform})




def warren(request):
    queryset = Warren.objects.filter(source__isnull=True).prefetch_related('consumer')
    dateform = DateForm(request.GET or None)
    if dateform.is_valid():
        date = dateform.cleaned_data.get('date',datetime.date.today())
    else:
        date = datetime.date.today()
    queryset = queryset.filter(date=date)
    factory = WarrenFactory(request.POST or None, queryset=queryset,initial=[{'date':date}])
    for form in factory:
        instance=form.instance or None
        form_queryset=form.instance.consumer.all()
        form.factory = WarrenTTOFactory(request.POST or None, instance=instance,queryset=form_queryset,prefix=form.prefix+'-factory')
    if request.method == 'POST':
        for form in factory:
            if form.is_valid():
                form.save()
                if form.factory.is_valid():
                    form.factory.save()
        if all([form.is_valid() for form in factory]) and all([form.factory.is_valid() for form in factory]):
            return redirect(reverse('make:warren')+'?date=%s' % date.isoformat())
    return render(request,'make/warren.html',dict(factory=factory,date=date,dateform=dateform))
