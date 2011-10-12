# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404,redirect
from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q,Sum,F
from whs.bill.models import Bill,Sold,Transfer
from whs.brick.models import Brick,BrickTable
from whs.brick.forms import BrickFilterForm
from whs.bill.forms import Bills
from datetime import date
from whs.bill.stores import BillStore,BrickStore
from whs.brick.stores import BricksStore,BrickSelectStore

@require_http_methods(["GET",])
def main(request):
    """
    Главная страница
    """
    return render(request, 'main.html',{'bills':Bill.objects.all()[:5]})

@require_http_methods(["GET",])
def form_get(request,form,id=None):
    """
    Вывод формы
    """
    if id:
        form = form(instance=get_object_or_404(form._meta.model,pk=id))
    else:
        form = form()
    if request.is_ajax():
        return HttpResponse(form)
    else:
        return render(request, form._meta.model.__name__+".html", {'form':form})

@require_http_methods(["POST",])
def form_post(request,form,id=None):
    """
    Универсальное представление для обработки пост данных формы
    """
    if id:
        form = form(request.POST,instance=get_object_or_404(form._meta.model,pk=id))
    else:
        form = form(request.POST)
    if form.is_valid():
            form.save()
            id = form.instance.pk
    if request.is_ajax():
        response = HttpResponse(simplejson.dumps({'success':form.is_valid(),'errors':form.errors,'id':id}))
    else:
        response = render(request, form._meta.model.__name__+".html", {'form':form})
    return response

@require_http_methods(["GET",])
def bills(request):
    """
    Предствление для таблицы с накладными, формой для фильтрации.
    """
    f = Bills(request.GET)
    return render(request, 'bills.html',{'form':f,'path':request.GET.urlencode()})

@require_http_methods(["GET",])
def bill_store(request):
    """
    Представление для dojo store накладных.
    """
    store = BillStore()
    f = Bills(request.GET)
    query = Bill.objects.all()
    if f.is_valid():
        brick = f.cleaned_data.pop('brick')
        for key,value in f.cleaned_data.items():
            if value:
                query = query.filter(**{key:value})
        if brick:
            query = query.filter(bill_sold_related__brick=brick).annotate()

    store.Meta.objects=query[:30]
    return HttpResponse(store.to_json(), mimetype='application/json')

@require_http_methods(["GET",])
def bricks(request):
    """
    Представление для отображение шаблона сводной таблицы
    """
    return render(request, 'bricks.html',{'form':BrickFilterForm()})

@require_http_methods(["GET",])
def agents(request):
    return render(request, 'agents.html')


@require_http_methods(["GET",])
def bricks_store(request):
    """
    Представление для dojo store сводной таблицы кирпича.
    """
    store = BricksStore()
    sold = Sold.objects.filter(doc__date__month=date.today().month,doc__date__year=date.today().year).values('brick').annotate(s=Sum('amount'))
    t_from = Transfer.objects.filter(doc__date__month=date.today().month,doc__date__year=date.today().year).values('brick').annotate(s=Sum('amount'))
    t_to = Transfer.objects.filter(doc__date__month=date.today().month,doc__date__year=date.today().year).values('sold__brick').annotate(s=Sum('amount'))
    sold = dict(map(lambda x: [x['brick'],x['s']],sold))
    t_from = dict(map(lambda x: [x['brick'],x['s']],t_from))
    t_to = dict(map(lambda x: [x['sold__brick'],x['s']],t_to))
    for b in store.Meta.objects:
        b.sold = sold.get(b.pk,0)
        b.plus = 0
        b.t_from = t_from.get(b.pk,0)
        b.t_to = t_to.get(b.pk,0)
        b.begin = b.total + b.sold + b.t_from - b.t_to
    return HttpResponse(store.to_json(), mimetype='application/json')


def brick_store(request,id):
    """
    Операции за месяц с определённым кирпичем.
    """
    len = 30
    brick = get_object_or_404(Brick,pk=id)
    store = {'label':'label','identifier':'id','items':[]}
    sold = map(lambda x: {'sold':x.amount,'date':x.doc.date.isoformat(),'id':x.get_id()},Sold.objects.filter(brick=brick)[:30])
    t_from = map(lambda x: {'t_from':x.amount,'date':x.doc.date.isoformat(),'id':x.get_id()},Transfer.objects.filter(brick=brick)[:30])
    t_to = map(lambda x: {'t_to':x.amount,'date':x.doc.date.isoformat(),'id':x.get_id()},Transfer.objects.filter(sold__brick=brick)[:30])
    store['items'].extend(sold)
    store['items'].extend(t_to)
    store['items'].extend(t_from)
    store['items'] = sorted(store['items'],key=lambda x: x['date'])
    return HttpResponse(simplejson.dumps(store), mimetype='application/json')


def brick_select(request):
    store = BrickSelectStore()
    return HttpResponse(store.to_json(), mimetype='application/json')
