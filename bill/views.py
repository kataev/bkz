from django.shortcuts import render, get_object_or_404,redirect
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from whs.bill.models import Bill

@require_http_methods(["GET",])
def bill_form_get(request,form,id=None):
    if id:
        form = form(instance=get_object_or_404(form._meta.model,pk=id))
    else:
        form = form()
    if request.is_ajax():
        return HttpResponse(form)
    else:
        return render(request, "Bill.html", {'form':form})

@require_http_methods(["POST",])
def bill_form_post(request,form,id=None):
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
        response = render(request,form._meta.model.__name__+".html", {'form':form})
    return response

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
def opers_form_post(request,form,id=None):
#    print request.POST
    if id:
        form = form(request.POST,instance=get_object_or_404(form._meta.model,pk=id))
        if form.is_valid():
            form.save()
    else:
        form = form(request.POST)
        if form.is_valid():
            form.save()
            bill = form.cleaned_data['bill']
            getattr(bill,form._meta.model.__name__.lower()).add(form.instance)
            bill.save()
    if request.is_ajax():
        response = HttpResponse(simplejson.dumps({'success':form.is_valid(),'errors':form.errors,'id':form.instance.pk}))
    else:
        response = render(request,form._meta.model.__name__+".html", {'form':form})
    return response

@require_http_methods(["POST",])
def finish_transfer(request,form):
    form = form(request.POST)
    print form.is_valid()
    if form.is_valid():
        form.cleaned_data['transfer'].sold = form.cleaned_data['sold']
        form.cleaned_data['transfer'].save()
    return HttpResponse(simplejson.dumps({'success':form.is_valid(),'errors':form.errors}))


@require_http_methods(["POST",])
def delete(request,form,model,id):
    form = form(request.POST)
    if form.is_valid() and form.cleaned_data['confirm']:
        get_object_or_404(model,pk=id).delete()
    return HttpResponse(simplejson.dumps({'success':form.is_valid(),'errors':form.errors}))