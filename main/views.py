# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import render_to_string
from cjson import encode as json
import datetime
import csv
from django.shortcuts import redirect
from whs.bricks.models import *
from whs.bills.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.core import  serializers
    
def main(response):
    models = {'bills':bills,'bricks':bricks,'solds':solds,'transfers':transfers}
    def f(model):
        return models[model]._meta.verbose_name_plural

    rendered = render_to_string('main.html',{'models':map(f,models)})
    return HttpResponse(rendered,mimetype="text/html;charset=utf-8")


def rest(response,modelName,id_str):
    model = {'bricks':bricks,'bills':bills,'solds':solds,'transfers':transfers}[modelName]
    id=[]

    for i in id_str.split('/'):
            id.append(i)

    if len(id_str)==0:
        query = model.objects.all()
    else:
        query = model.objects.filter(pk__in=id)

    return HttpResponse(serializers.serialize('json',query),mimetype="text/html;charset=utf-8")

def test(response):
    response= HttpResponse(json({'test':'test'}),mimetype="application/json; charset=utf-8")
    response.status_code=400
    return response

def form(request,modelName,id=0):
    model = {'bricks':bricks,'bills':bills,'solds':solds,'transfers':transfers}[modelName]
    form = {'bricks':brickForm,'bills':billForm,'solds':soldForm,'transfers':transferForm}[modelName]

    modelType=model.__base__.__name__

#    if modelName not in models.keys():
#        return HttpResponse(json({'status':'error','message':'DoesNotExist'}),mimetype="application/json;charset=utf-8")

    if request.method == 'GET':

        if int(id)==0:
            f=form()
            method='POST'
            url = 'form/%s/' % modelName
            if modelName in ('bricks','transfers',):
                title=u'Новый %s' % model._meta.verbose_name.lower()
            else:
                title=u'Новая %s' % model._meta.verbose_name.lower()
        else:
            url = 'form/%s/%s/' % (modelName,id)
            method='PUT'
            title=u'%s %s' % (model._meta.verbose_name,id)
            try:
                f=form(instance=model.objects.get(pk=id))
            except ObjectDoesNotExist:
                return HttpResponse(json({'status':'error','message':'DoesNotExist'}),mimetype="application/json;charset=utf-8")
            method='PUT'

        if modelName in ['solds','transfers']:
            temp='opers.html'
        else:
            temp='form.html'

        if request.is_ajax():
            rendered = render_to_string(temp,{'form':f,'url':url,'method':method,'title':title})
            return HttpResponse(json({'modelType':modelType,'method':method,'title':title,'html':rendered}),mimetype="text/html;charset=utf-8;")
        else:
            rendered = render_to_string(temp,{'modelType':modelType,'form':f,'url':'./','method':'POST','title':title})
            return HttpResponse(rendered,mimetype="text/html;charset=utf-8;")

    if request.method == 'POST' and int(id)==0:
        data=request.POST.copy() # Копируем массив, ибо request - read only
        for field in data:
            data[field]=data[field].replace(',','.')
        f = form(data)
        if f.is_valid():
            ins = f.save()
            return redirect(ins)
        else:
#            del form.errors['__all__']
            return HttpResponse(json(f.errors),mimetype="application/json;charset=utf-8")

    if int(id)!=0 and (request.method == 'POST' or request.method == 'PUT'):
        if request.method == 'POST':
            data=request.POST.copy()
        else:
            data=request.PUT.copy() # Копируем массив, ибо request - read only
        for field in data:
            data[field]=data[field].replace(',','.')
        print model.objects.get(pk=id)
        f = form(data,instance=model.objects.get(pk=id))
        if f.is_valid():
            ins = f.save()
            return redirect(ins)
        else:
#            del form.errors['__all__']
            return HttpResponse(json({'status':'error','message':f.errors}),mimetype="application/json;charset=utf-8")

    if request.method == 'DELETE':
        if id == 0:
            return HttpResponse(json({'status':'error','message':'Нельзя удалять объект с id = 0'}),mimetype="application/json;charset=utf-8")
        else:
            model.objects.get(pk=id).delete()
            return HttpResponse(json({'status':'deleted','id':id}),mimetype="application/json;charset=utf-8")
