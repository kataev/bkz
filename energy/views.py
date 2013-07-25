# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render

from bkz.whs.forms import YearMonthFilter
from bkz.energy.models import Energy, Teplo
from bkz.energy.forms import EnergyFactory, TeploFactory

from itertools import tee, izip


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


def delta(queryset, fields=None):
    return ([(c[k] - p[k]) / (c['date'] - p['date']).days for k in p.keys() if k not in {'date', 'id'}] for c, p in
            pairwise(queryset))


def index(request, year=None, month=None):
    fields = ('gaz', 'elec4', 'elec16')
    start = datetime.date.today().replace(day=1)
    energy = []
    prev = 0
    for v in Energy.objects.filter(date__gte=start).reverse():
        if not prev:
            prev = Energy.objects.filter(date__lt=v.date)[:1][0]
        o = [v.date, ]
        for f in fields:
            o.append((getattr(v, f) - getattr(prev, f)) / ((v.date - prev.date).days or 1))
        energy.append(o)
        prev = v
    return render(request, 'energy/index.html', dict(opers=[energy]))


def energy(request):
    datefilter = YearMonthFilter(request.GET or None, model=Energy)
    date = datefilter.get_date
    data = {'date__year': date.year}
    if datefilter.is_valid() and datefilter.cleaned_data.get('date__month') is not None:
        data['date__month'] = date.month
    queryset = Energy.objects.filter(**data).reverse()
    initial = [{'datetime': datetime.date.today()}, ]
    energy = EnergyFactory(request.POST or None, queryset=queryset, initial=initial)
    return render(request, 'energy/energy.html', dict(object_list=energy, datefilter=datefilter, date=date))


def teplo(request):
    datefilter = YearMonthFilter(request.GET or None, model=Teplo)
    date = datefilter.get_date
    data = {'date__year': date.year}
    if datefilter.is_valid() and datefilter.cleaned_data.get('date__month') is not None:
        data['date__month'] = date.month
    queryset = Teplo.objects.filter(**data)
    initial = [{'datetime': datetime.date.today()}, ]
    energy = TeploFactory(request.POST or None, queryset=queryset, initial=initial)
    return render(request, 'energy/teplo.html', dict(object_list=energy, datefilter=datefilter, date=date))
