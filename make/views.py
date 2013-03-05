# -*- coding: utf-8 -*-
import datetime
from itertools import groupby,tee
from operator import itemgetter,attrgetter

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from bkz.log import construct_change_message, log_addition, log_change, log_deletion

from bkz.lab.models import Cause
from bkz.make.models import Forming, Warren
from bkz.make.forms import FormingFactory, WarrenFactory, WidthColorForm
from bkz.whs.forms import DateForm, YearMonthFilter


def index(request):
    datefilter = YearMonthFilter(request.GET or None, model=Forming)
    forming = Forming.objects.select_related('width','warren').prefetch_related('bar', 'raw', 'half')
    if datefilter.is_valid():
        data = dict(filter(itemgetter(1), datefilter.cleaned_data.items()))
    else:
        date = datetime.date.today()
        data = dict(date__year=date.year, date__month=date.month)
    forming = forming.filter(**data)
    warren = Warren.objects.filter(**data).select_related('forming').prefetch_related('forming__bar', 'forming__raw', 'forming__half')
    warren = dict((d,list(warren)) for d,warren in groupby(warren, key=attrgetter('date')))
    object_list = tuple((d, list(forming),warren.get(d,[])) for d, forming in groupby(forming, key=attrgetter('date')))
    return render(request, 'make/index.html', {'datefilter': datefilter, 'object_list': object_list})


def forming(request):
    dateform = DateForm(request.GET or None)
    if dateform.is_valid():
        date = dateform.cleaned_data.get('date', datetime.date.today())
    else:
        date = datetime.date.today()
    filter = {'date': date}
    queryset = Forming.objects.filter(**filter).prefetch_related('bar', 'raw', 'half')
    order = tuple(f.order for f in queryset)
    if order:
        order = max(order) + 1
    else:
        order = 1
    initial = [{'date':date, 'order':i} for i in range(order, FormingFactory.extra + order + 1)]
    factory = FormingFactory(request.POST or None, initial=initial, queryset=queryset, prefix='forming')
    instance = queryset[0] if len(queryset) > 0 else None
    widthcolor = WidthColorForm(request.POST or None, instance=instance)
    if request.method == 'POST' and factory.is_valid() and widthcolor.is_valid():
        factory.save()
        Forming.objects.filter(date=date).update(**widthcolor.cleaned_data)
        messages.success(request, 'Формовка сохранена')
        return redirect(reverse('make:forming') + '?date=%s&success=True' % date.isoformat())
    return render(request, 'make/forming.html', {'factory': factory, 'date': date, 'dateform': dateform, 'widthcolor': widthcolor})


def warren(request):
    dateform = DateForm(request.GET or None)
    if dateform.is_valid():
        date = dateform.cleaned_data.get('date', datetime.date.today())
    else:
        date = datetime.date.today()
    timedelta = datetime.timedelta(10)
    queryset = Warren.objects.filter(date=date).select_related('forming','forming__width').prefetch_related('part','part__batch','part__rows','part__batch__width','cause')
    order = tuple(f.order for f in queryset)
    if order:
        order = max(order) + 1
    else:
        order = 1
    initial = [{'date':date, 'order':i} for i in range(order, WarrenFactory.extra + order + 1)]
    factory = WarrenFactory(request.POST or None, queryset=queryset, initial=initial, prefix='tto')

    if request.method == 'POST' and factory.is_valid():
        factory.save()
        source = Warren.objects.filter(tto__isnull=False,date=date-datetime.timedelta(1)).latest('order')
        for w in Warren.objects.filter(date=date).filter(cause__isnull=True).order_by('order'):
            if w.tto:
                source = w
            w.source = source
            try:
                w.forming = Forming.objects.filter(date__lt=w.date,date__gt=w.date-timedelta).filter(tts=w.tts).order_by('-date')[0]
            except IndexError:
                messages.error(request, 'Телеги №%d нет в формовке' % w.tts)
            w.save()
        messages.success(request, 'Садка сохранена')
        return redirect(reverse('make:warren') + '?date=%s&s=1' % date.isoformat())
    cause = Cause.objects.filter(type='warren')
    for form in factory:
        form.fields['cause'].queryset = cause
    return render(request, 'make/warren.html', dict(factory=factory, date=date, dateform=dateform))
