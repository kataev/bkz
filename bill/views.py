# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404,redirect
from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from stores import *
from models import Bill
from random import Random

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
        form = form(instance=get_object_or_404(form._meta.model,pk=id),auto_id="id_%s_%%s" % id)
    else:
        id = Random().randint(0,100000)
        form = form(auto_id="id_%s_%%s" % id)
    if request.is_ajax():
        return HttpResponse(form)
    else:
        return render(request, "Bill.html", {'form':form})

@require_http_methods(["GET",])
def bill_store(request,form,id):
    """ Представление для вывода dojo store операций накладной в виде дерева """
    print id
    if id:
        bill = get_object_or_404(form._meta.model,pk=id)
        store = BillStore()
        for s in store.Meta.stores:
            s.Meta.objects= s.Meta.objects.model.objects.filter(doc=bill)
    else:
        store = BillStore()
        store.Meta.objects = store.Meta.objects.empty()

    return HttpResponse(store.to_json(), mimetype='application/json')

@require_http_methods(["GET",])
def opers_form_get(request,form,id=None):
    """ Представление для вывода формы операций """
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
    """ Представление для обработки POST данных формы """

    if id: form = form(request.POST,instance=get_object_or_404(form._meta.model,pk=id))
    else: form = form(request.POST)
    if form.is_valid():
        model = form.save()
        if model._meta.module_name == 'bill':
            if form.cleaned_data['sold']: form.cleaned_data['sold'].update(doc=model)
            if form.cleaned_data['transfer']: form.cleaned_data['transfer'].update(doc=model)
        id = '%s.%s__%d' % (form._meta.model._meta.app_label,form._meta.model._meta.module_name,model.pk or 0)
    print request.POST,form.errors
    return HttpResponse(simplejson.dumps({'success':form.is_valid(),'errors':form.errors,
                                          'id': id}))

@require_http_methods(["POST", ])
def delete(request,form,model,id):
    """ Представление для удоления операций. //TODO: переписать.на rest или с выбором любой модели. """
    form = form(request.POST)
    if form.is_valid() and form.cleaned_data['confirm']:
        get_object_or_404(model,pk=id).delete()
    return HttpResponse(simplejson.dumps({'success':form.is_valid(),'errors':form.errors}))