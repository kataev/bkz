from django.shortcuts import render, get_object_or_404,redirect
from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from stores import SoldStore

@require_http_methods(["GET",])
def bill_form_get(request,form,id=None):
    if id:
        bill = get_object_or_404(form._meta.model,pk=id)
        form = form(instance=bill)
        sold = bill.bill_sold_related.all()
        transfer = bill.bill_transfer_related.all()
    else:
        form = form()
        sold = None
        transfer = None
    if request.is_ajax():
        return HttpResponse(form)
    else:
        return render(request, "Bill.html", {'form':form,'sold':sold,'transfer':transfer})

@require_http_methods(["GET",])
def bill_store(request,form,id):
    bill = get_object_or_404(form._meta.model,pk=id)
    store = SoldStore()
    store.Meta.objects = bill.bill_sold_related.all()
    return HttpResponse(store.to_json(), mimetype='application/json')

@require_http_methods(["GET",])
def opers_form_get(request,form,id=None):
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
    if id:
        form = form(request.POST,instance=get_object_or_404(form._meta.model,pk=id))
        if form.is_valid():
            form.save()
    else:
        form = form(request.POST)
        if form.is_valid():
            form.save()
    if request.is_ajax():
        response = HttpResponse(simplejson.dumps({'success':form.is_valid(),'errors':form.errors,'id':form.instance.pk}))
    else:
        response = render(request,form._meta.model.__name__+".html", {'form':form})
    return response

@require_http_methods(["POST",])
def delete(request,form,model,id):
    form = form(request.POST)
    if form.is_valid() and form.cleaned_data['confirm']:
        get_object_or_404(model,pk=id).delete()
    return HttpResponse(simplejson.dumps({'success':form.is_valid(),'errors':form.errors}))