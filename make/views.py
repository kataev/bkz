# -*- coding: utf-8 -*-
import datetime
from itertools import groupby
from operator import itemgetter

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from bkz.make.models import Forming, Warren
from bkz.make.forms import FormingFactory, WarrenFactory, WidthColorForm
from bkz.whs.forms import DateForm, YearMonthFilter


def index(request):
    datefilter = YearMonthFilter(request.GET or None, model=Forming)
    if datefilter.is_valid():
        data = dict((k, v) for k, v in datefilter.cleaned_data.items() if v)
    else:
        date = datetime.date.today()
        data = dict(date__year=date.year, date__month=date.month)
    forming = Forming.objects.filter(**data).values_list('date', 'pk', 'tts', 'empty', 'warren')
    warren = Warren.objects.filter(cause__isnull=True).filter(**data).values_list('date', 'pk')
    warren = dict((d, list(warren)) for d, warren in groupby(warren, key=itemgetter(0)))
    object_list = [(d, tuple(forming), warren.get(d, ())) for d, forming in groupby(forming, key=itemgetter(0))]
    return render(request, 'make/index.html', {'datefilter': datefilter, 'object_list': object_list})


def forming(request):
    dateform = DateForm(request.GET or None)
    if dateform.is_valid():
        date = dateform.cleaned_data.get('date', datetime.date.today())
    else:
        date = datetime.date.today()
    filter = {'date': date}
    queryset = Forming.objects.filter(**filter).prefetch_related('bars', 'raws', 'halfs')
    order = max(f.order for f in queryset or (Forming(),)) + 1
    initial = [{'date': date, 'order': i} for i in range(order, FormingFactory.extra + order + 1)]
    factory = FormingFactory(request.POST or None, initial=initial, queryset=queryset, prefix='forming')
    instance = queryset[0] if len(queryset) > 0 else None
    widthcolor = WidthColorForm(request.POST or None, instance=instance)
    if request.method == 'POST' and factory.is_valid() and widthcolor.is_valid():
        factory.save()
        Forming.objects.filter(date=date).update(**widthcolor.cleaned_data)
        messages.success(request, 'Формовка сохранена')
        return redirect(reverse('make:forming') + '?date=%s&success=True' % date.isoformat())
    return render(request, 'make/forming.html',
                  {'factory': factory, 'date': date, 'dateform': dateform, 'widthcolor': widthcolor})


def warren(request):
    dateform = DateForm(request.GET or None)
    if dateform.is_valid():
        date = dateform.cleaned_data.get('date', datetime.date.today())
    else:
        date = datetime.date.today()
    timedelta = datetime.timedelta(20)
    delay = datetime.timedelta(1)
    queryset = Warren.objects.filter(date=date).select_related('forming', 'forming__width', 'part').prefetch_related(
        'part__batch', 'part__rows', 'part__batch__width', 'cause')
    order = max(f.order for f in queryset or (Warren(),)) + 1
    initial = [{'date': date, 'order': i} for i in range(order, WarrenFactory.extra + order + 1)]
    factory = WarrenFactory(request.POST or None, queryset=queryset, initial=initial, prefix='tto')
    if request.method == 'POST' and factory.is_valid():
        factory.save()
        try:
            source = Warren.objects.filter(tto__isnull=False, date=date - datetime.timedelta(1)).latest('order')
        except Warren.DoesNotExist:
            source = None
        for w in Warren.objects.filter(date=date).order_by('order'):
            if w.tto:
                source = w
            w.source = source
            try:
                w.forming = Forming.objects.filter(date__lt=w.date - delay, date__gte=w.date - timedelta).filter(tts=w.tts,warren__isnull=True).order_by('-date')[0]
            except IndexError:
                pass
            w.save()
        messages.success(request, 'Садка сохранена')
        return redirect(reverse('make:warren') + '?date=%s&s=1' % date.isoformat())
    return render(request, 'make/warren.html', dict(factory=factory, date=date, dateform=dateform))