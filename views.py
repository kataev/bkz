# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404,redirect
from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q,Sum
from whs.bill.models import Bill,Sold,Transfer
from whs.brick.models import BrickTable
from whs.brick.forms import BrickFilterForm
from whs.bill.forms import Bills
from datetime import date

@require_http_methods(["GET",])
def form_get(request,form,id=None):
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

def main(request):
    return render(request, 'main.html',{'bills':Bill.objects.all()[:5]})

def bills(request):
    f = Bills(request.GET)
    query = Bill.objects.all()
    if f.is_valid():
        for a in f.cleaned_data:
            if f.cleaned_data[a]:
                if a == 'brick':
                    b = f.cleaned_data[a]
                    query = query.filter(Q(sold__brick=b) or Q(transfer__brick=b))
                else:
                    query = query.filter(**{a:f.cleaned_data[a]})
    return render(request, 'bills.html', {'bills':query,'form':f})


def bill_store(request):
    from whs.bill.stores import BillSoldStore
    store = BillSoldStore()
    f = Bills(request.GET)
    query = Bill.objects.all()
    if f.is_valid():
        for a in f.cleaned_data:
            if f.cleaned_data[a]:
                if a == 'brick':
                    b = f.cleaned_data[a]
                    query = query.filter(Q(bill_sold_related__brick=b) or Q(bill_transfer_related__brick=b))
                else:
                    query = query.filter(**{a:f.cleaned_data[a]})
    store.Meta.stores[0].Meta.objects=query
#    store.Meta.stores[1].Meta.objects=Sold.objects.filter(pk__in=query.values_list('pk'))
#    store.Meta.stores[1].Meta.stores[0].Meta.objects=Transfer.objects.filter(pk__in=query.values_list('pk'))

    return HttpResponse(store.to_json(), mimetype='application/json')



def bricks(request):
    return render(request, 'bricks.html',{'form':BrickFilterForm()})

def brick_store(request):
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
        if not b.t_from == 0:
            print b
    return HttpResponse(store.to_json(), mimetype='application/json')