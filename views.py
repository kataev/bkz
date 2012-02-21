# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404,redirect
from django.views.decorators.http import require_http_methods

from whs.manufacture.forms import *
from whs.bill.forms import *

@require_http_methods(["GET",])
def main(request):
    """ Главная страница """
    return render(request, 'index.html')

def journal(request):
    form = DateForm(request.GET or None)
    if form.is_valid(): date = form.cleaned_data.get('date')
    else: date = datetime.date.today()

    Jounal = list(Bill.objects.select_related().filter(date=date))+list(Man.objects.select_related().filter(date=date))

    return render(request,'journal.html',dict(Journal=Jounal,date=form))

def flat_form(request,Form,id):
    """ Форма  """
#    id = args[0]
    if id: model = get_object_or_404(Form._meta.model,pk=id)
    else: model = None
    if request.method == 'POST':
        form = Form(request.POST,instance=model)
        if form.is_valid():
            model = form.save()
            return redirect(model)
    else:
        form = Form(instance=model)

    return render(request, 'flat-form.html',dict(form=form))

def history(request):
    if request.POST:
        for b in Brick.objects.order_by('pk').all():
            date=datetime.date.today().replace(day=1)
            h = History(brick=b,date=date)
            for f in ['begin', 'add', 't_from', 't_to', 'sold', 'total']:
                setattr(h,f,getattr(b,f))
            h.save()
            b.begin = b.total
            for f in [ 'add', 't_from', 't_to', 'sold', 'total']:
                setattr(b,f,0)
            b.save()
        return redirect('/')
    date = datetime.date.today().replace(day=1)
    if date.month == 12:
        date = date.replace(year=date.year-1,month=1)
    f = DateForm(request.GET or None,initial={'date':date})
    if f.is_valid():
        date = f.cleaned_data.get('date').replace(day=1)

    history = History.objects.filter(date=date)

    dates = History.objects.dates('date','month')

    return render(request,'history.html',dict(History=history,date=dates))