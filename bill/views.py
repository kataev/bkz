from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from whs.bill.models import Bill

@require_http_methods(["GET",])
def bill_form_get(request,form,id=None):
    if id:
        form = form(instance=form._meta.model.objects.get(pk=id))
    else:
        form = form()
    if request.is_ajax():
        return HttpResponse(form)
    else:
        return render_to_response("bill/Bill.html", {'form':form} , context_instance=RequestContext(request))

def bill_form_post(request,form,id=None):
    if id:
        form = form(request.POST,instance=form._meta.model.objects.get(pk=id))
    else:
        form = form(request.POST)
    if form.is_valid():
            form.save()
    if request.is_ajax():
        response = HttpResponse(simplejson.dumps({'success':form.is_valid(),'errors':form.errors}))
    else:
        response = render_to_response("bill/"+form._meta.model.__name__+".html", {'form':form}, context_instance=RequestContext(request))
    return response

def opers_form_get(request,form,id=None):
    if id:
        form = form(instance=form._meta.model.objects.get(pk=id))
    else:
        form = form(request.GET)
    if request.is_ajax():
        return HttpResponse(form)
    else:
        return render_to_response("bill/"+form._meta.model.__name__+".html", {'form':form}, context_instance=RequestContext(request))

@require_http_methods(["POST",])
def opers_form_post(request,form,id=None):
    print request.POST
    if id:
        form = form(request.POST,instance=form._meta.model.objects.get(pk=id))
        if form.is_valid():
            form.save()
    else:
        form = form(request.POST)
        if form.is_valid():
            form.save()
            bill = Bill.objects.get(pk=form.cleaned_data['bill'])
            getattr(bill,form._meta.model.__name__.lower()+'s').add(form.instance)
            bill.save()
    if request.is_ajax():
        response = HttpResponse(simplejson.dumps({'success':form.is_valid(),'errors':form.errors,'id':form.instance.pk}))
    else:
        response = render_to_response("bill/"+form._meta.model.__name__+".html", {'form':form}, context_instance=RequestContext(request))
    return response

@require_http_methods(["POST",])
def finish_transfer(request,form):
    form = form(request.POST)
    print form.is_valid()
    if form.is_valid():
        form.cleaned_data['transfer'].sold = form.cleaned_data['sold']
        form.cleaned_data['transfer'].save()
    return HttpResponse(simplejson.dumps({'success':form.is_valid(),'errors':form.errors}))