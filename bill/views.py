from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from whs.bill.models import Bill

@require_http_methods(["GET",])
def form(request,form,id=None):
    if id:
        form = form(instance=form._meta.model.objects.get(pk=id))
    else:
        if 'bill' in request.GET:
            form = form({'bill':request.GET['bill']})
        else:
            form = form()

    if request.is_ajax():
        return HttpResponse(form)
    else:
        return render_to_response("bill/"+form._meta.model.__name__+".html", {'form':form} , context_instance=RequestContext(request))

#@require_http_methods(["POST",])
def post(request,form,id=None,bill=None):
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