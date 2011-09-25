# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404,redirect
from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q,Sum,F
from whs.bill.models import Bill,Sold,Transfer
from whs.brick.models import Brick
from whs.brick.forms import BrickFilterForm
from whs.bill.forms import Bills
from datetime import date
from whs.bill.stores import BillStore,BrickStore

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
        print f.cleaned_data
        brick = f.cleaned_data.pop('brick')
        for key,value in f.cleaned_data.items():
            if value:
                query = query.filter(**{key:value})
                print key,values,query

        if brick:
#            sold = Sold.objects.filter(brick=brick,doc=query).values('pk')
            print query
            query = query.filter(bill_sold_related__brick=brick).annotate()
        print query
        
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
    from whs.brick.stores import BrickStore
    store = BrickStore()
    bills = Bill.objects.filter(date__month=date.today().month).values_list('pk')
#    store.Meta.objects = BrickTable.objects.filter(mark__in=[100,125])
    solds = Sold.objects.filter(doc__in=bills)
    trans = Transfer.objects.filter(doc__in=bills)
    print len(solds),len(trans)
    for b in store.Meta.objects:
        b.sold = solds.filter(brick=b).aggregate(s=Sum('amount')).values()[0] or 0
        b.t_from = trans.filter(brick=b).aggregate(s=Sum('amount')).values()[0] or 0
        b.t_to = trans.filter(sold__brick=b).aggregate(s=Sum('amount')).values()[0] or 0
        b.begin = b.total + b.sold + b.t_from - b.t_to
    return HttpResponse(store.to_json(), mimetype='application/json')


def brick_store(request,id=None):
    brick = get_object_or_404(Brick,pk=id)
    store = BrickStore()
    store.Meta.objects = Sold.objects.filter(brick=brick)
    return HttpResponse(store.to_json(), mimetype='application/json')