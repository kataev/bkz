from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.utils import simplejson
from django.http import HttpResponse

def form(request,form,id=None):
    if request.method == 'POST': # If the form has been submitted...
        if id:
            form = ContactForm(request.POST,instance=form._meta.model.objects.get(pk=id)) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                form.save()
            if request.is_ajax():
                response = {'success':form.is_valid(),'errors':form.errors}
                return HttpResponse(simplejson.dumps(response))
            else:
                return render_to_response("bills/"+form._meta.model.__name__+".html", {'form':form}, context_instance=RequestContext(request))
        else:
            pass

    else:
        if id:
            form = form(instance=form._meta.model.objects.get(pk=id))
        else:
            form = form()
        if request.is_ajax():
            return HttpResponse(form)
        else:
            return render_to_response("bills/"+form._meta.model.__name__+".html", {'form':form}, context_instance=RequestContext(request))