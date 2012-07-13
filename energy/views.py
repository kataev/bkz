# -*- coding: utf-8 -*-
import datetime
from copy import deepcopy

from django.shortcuts import render, get_object_or_404,redirect

from bkz.energy.models import Energy, Teplo, reverse


def delta(queryset,fields):
    prev = 0
    energy = []
    for v in queryset.reverse():
        if not prev:
            prev = v
            continue
        o = deepcopy(v)
        for f in fields[1:]:
            setattr(o,f,abs(getattr(v,f) - getattr(prev,f)) / ((v.date-prev.date).days or 1))
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
            o.append( (getattr(v,f) - getattr(prev,f)) / ((v.date-prev.date).days or 1))
        energy.append(o)
        prev = v

    return render(request,'chart.html',dict(opers=[energy]))

def data(request,Form,id=None,date=None):
    """ Форма  """
    #    id = args[0]
    if id:
        model = get_object_or_404(Form._meta.model,pk=id)
        if request.method == 'POST':
            form = Form(request.POST,instance=model)
            if form.is_valid():
                model = form.save()
                return redirect(model.get_absolute_url())
        else:
            form = Form(initial=request.GET.dict() or {'date':datetime.date.today()},instance=model)
            return render(request, 'flat-form.html',dict(form=form))
    else:
        if request.method == 'POST':
            form = Form(request.POST)
            if form.is_valid():
                model = form.save()
                return redirect(reverse('energy:%s' % Form._meta.model.__name__))
        else:
            form = Form(initial=request.GET.dict() or {'date':datetime.date.today()})
    data = Form._meta.model.objects.all()[:31]
    return render(request, 'energy.html',dict(form=form,data=data))