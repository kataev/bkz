# -*- coding: utf-8 -*-
import datetime
from copy import deepcopy

from django.shortcuts import render, get_object_or_404,redirect

from whs.energy.models import Energy, Teplo


def delta(queryset,fields):
    prev = 0
    energy = []
    for v in queryset.reverse():
        if not prev:
            prev = v
            continue
        o = deepcopy(v)
        for f in fields[1:]:
            setattr(o,f,abs(getattr(v,f) - getattr(prev,f)) / (v.date-prev.date).days )
        energy.append(o)
        prev = v
    return energy

def main(request,year=None,month=None):
    fields = ('gaz','elec4','elec16')
    start = datetime.date.today().replace(day=1)
    energy = []
    prev = 0
    for v in Energy.objects.filter(date__gte=start).reverse():
        if not prev:
            prev = Energy.objects.filter(date__lt=v.date)[:1][0]
        o = [v.date,]
        for f in fields:
            o.append( (getattr(v,f) - getattr(prev,f)) / (v.date-prev.date).days )
        energy.append(o)
        prev = v

    return render(request,'energy.html',dict(opers=[energy]))