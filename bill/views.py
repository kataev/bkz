# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404,redirect
from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from stores import SoldStore
from models import Bill

@require_http_methods(["GET",])
def bill_get(request, year=None, number=None):
    """
    ЧПУ для накладной
    """
    if len(year) == 2: year = '20'+year
    bill = get_object_or_404(Bill,date__year=year,number=number)
    return redirect('/bill/%d/' % bill.id)


@require_http_methods(["GET",])
def bill_form_get(request,form,id=None):
    """
    Представление для вывода формы накладной.
    """
    if id:
        bill = get_object_or_404(form._meta.model,pk=id)
        form = form(instance=bill)
    else:
        form = form()
    if request.is_ajax():
        return HttpResponse(form)
    else:
        return render(request, "Bill.html", {'form':form})

@require_http_methods(["GET",])
def bill_store(request,form,id):
    """
    Представление для вывода dojo store операций накладной в виде дерева
    """
    bill = get_object_or_404(form._meta.model,pk=id)
    store = SoldStore()
    store.Meta.objects = bill.bill_sold_related.all()
#    store.Meta.objects = bill.bill_transfer_related.all()
    return HttpResponse(store.to_json(), mimetype='application/json')

@require_http_methods(["GET",])
def opers_form_get(request,form,id=None):
    """
    Представление для вывода формы операций
    """
    if id:
        form = form(instance=get_object_or_404(form._meta.model,pk=id))
    else:
        form = form(request.GET)
    if request.is_ajax():
        return HttpResponse(form)
    else:
        return render(request,form._meta.model.__name__+".html", {'form':form})

@require_http_methods(["POST",])
def form_post(request,form,id=None):
    """
    Представление для обработки POST данных формы
    """
    if id:
        form = form(request.POST,instance=get_object_or_404(form._meta.model,pk=id))
        if form.is_valid():
            print form.instance.brick.__dict__
            form.save()
    else:
        form = form(request.POST)
        if form.is_valid():
            form.save()
    if request.is_ajax():
        return HttpResponse(simplejson.dumps({'success':form.is_valid(),'errors':form.errors,'id':form.instance.pk}))

@require_http_methods(["POST",])
def delete(request,form,model,id):
    """
    Представление для удоления операций. //TODO: переписать.на rest или с выбором любой модели.
    """
    form = form(request.POST)
    if form.is_valid() and form.cleaned_data['confirm']:
        get_object_or_404(model,pk=id).delete()
    return HttpResponse(simplejson.dumps({'success':form.is_valid(),'errors':form.errors}))