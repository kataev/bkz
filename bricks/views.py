# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import render_to_string
from cjson import encode as json
import datetime
import csv
from whs.bricks.models import *

#def form(request):
#   if request.method == 'POST': # Если пост то обрабатываем данные
#        post=request.POST.copy() # Копируем массив, ибо request - read only
#        f=bricksForm
#
#        for field in post:
#            post[field]=post[field].replace(',','.')
#
#        form = f(post)
#
#        if form.is_valid():
#            inst = form.save()
#            return HttpResponse(json({'status':'ok','id':inst.pk}),mimetype="application/json;charset=utf-8")
#        else:
#            del form.errors['__all__']
#            return HttpResponse(json({'status':'error','message':form.errors}),mimetype="application/json;charset=utf-8")
#    else:
#        rendered = render_to_string('form.html',{'energy_form':energyForm(prefix='energy').as_ul(),'teplo_form':teploForm(prefix='teplo').as_ul()})
#        return HttpResponse(rendered,mimetype="text/html;charset=utf-8;")
#
#
#def forms(request):
