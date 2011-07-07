# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.views.decorators.http import require_http_methods
#from django.db.models.loading import get_models, get_app

from whs.bricks.models import *
from whs.bills.models import *

from dojango.util import dojo_collector
from dojango.decorators import json_response

def main(request):
    return render_to_response('main.html',
                          context_instance=RequestContext(request))


def bill_add(request):
    f = billForm()
#    f.fields['solds'].widget.dojo_type='whs.select.sold'
#    f.fields['transfers'].widget.dojo_type='whs.select.transfer'
    dojo_collector.add_module("dijit.form.Form")
    dojo_collector.add_module("dijit.form.Button")

    return render_to_response('doc_add.html',{'form':f,'title':'Новая накладная'},
                          context_instance=RequestContext(request))

def sold_add(request):
    f = soldForm()
    dojo_collector.add_module("dijit.form.Form")
    dojo_collector.add_module("dijit.form.Button")
#    f.fields['brick'].widget.dojo_type='whs.select.brick'
    return render_to_response('doc_add.html',{'form':f,'title':'Новая отгрузка'},
                          context_instance=RequestContext(request))

#@require_http_methods(['POST'])
@json_response
def ajax_add(request,model_name):
    forms = {'bill':billForm,'sold':soldForm,'transfer':transferForm}
    try:
        form = forms[model_name]
    except KeyError:
        return {'error':'KeyError'}
    if request.is_ajax():
#        return {'test':True}
        data=request.POST.copy() # Копируем массив, ибо request - read only
        for field in data:
            data[field]=data[field].replace(',','.')
        f = form(data)
        if f.is_valid():
            ins = f.save()
            return {'status':True}
        else:
            return f.errors


    else:
        return 

#def show_bill(request):
#    store = billStore()
#    return HttpResponse(store.to_json(), mimetype='application/json')
#
#
#
#def main(response):
#    models = {'bills':bills,'bricks':bricks,'solds':solds,'transfers':transfers}
#    def f(model):
#        return models[model]._meta.verbose_name_plural
#
#    rendered = render_to_string('main.html',{'models':map(f,models)})
#    return HttpResponse(rendered,mimetype="text/html;charset=utf-8")
#
#
#def rest(request,modelName,id_str):
#
#    try:
#        model = {'bricks':bricks,'bills':bills,'solds':solds,'transfers':transfers}[modelName]
#    except KeyError:
#        return HttpResponse(json({'status':'error','message':'KeyError'}),mimetype="application/json;charset=utf-8")
#
#    id=[]
#
#    for i in id_str.split('/'):
#            id.append(i)
#    data = {}
#    data.update(request.GET.copy())
#    for val in data:
#        data[str(val)]=data.pop(val)
#
#    try:
#        if len(id_str)==0:
#            if len(request.GET) == 0:
#                query = model.objects.all()
#            else:
##                for val,key in data:
##                    print val,key
##                    data[val]=str(data.pop[val])
#                print data
#                query = model.objects.filter(**data)
#        else:
#            query = model.objects.filter(pk__in=id)
#    except (ValueError,TypeError),e:
#        return HttpResponse(json({'status':'error','message':str(e)}),mimetype="application/json;charset=utf-8")
#
#    return HttpResponse(serializers.serialize('json',query),mimetype="application/json;charset=utf-8")
#
#def test(response):
#    response= HttpResponse(json({'test':'test'}),mimetype="application/json; charset=utf-8")
#    response.status_code=400
#    return response
#
#def form(request,modelName,id=0):
#    model = {'bricks':bricks,'bills':bills,'solds':solds,'transfers':transfers}[modelName]
#    form = {'bricks':brickForm,'bills':billForm,'solds':soldForm,'transfers':transferForm}[modelName]
#
#    modelType=model.__base__.__name__
#
##    if modelName not in models.keys():
##        return HttpResponse(json({'status':'error','message':'DoesNotExist'}),mimetype="application/json;charset=utf-8")
#
#    if request.method == 'GET':
#
#        if int(id)==0:
#            f=form()
#            method='POST'
#            url = 'form/%s/' % modelName
#            if modelName in ('bricks','transfers',):
#                title=u'Новый %s' % model._meta.verbose_name.lower()
#            else:
#                title=u'Новая %s' % model._meta.verbose_name.lower()
#        else:
#            url = 'form/%s/%s/' % (modelName,id)
#            method='PUT'
#            title=u'%s %s' % (model._meta.verbose_name,id)
#            try:
#                f=form(instance=model.objects.get(pk=id))
#            except ObjectDoesNotExist:
#                return HttpResponse(json({'status':'error','message':'DoesNotExist'}),mimetype="application/json;charset=utf-8")
#            method='PUT'
#
#        if modelName in ['solds','transfers']:
#            temp=modelName+'.html'
#        else:
#            temp='form.html'
#
#        if request.is_ajax():
#            rendered = render_to_string(temp,{'form':f,'url':url,'method':method,'title':title,'ajax':True})
#            return HttpResponse(json({'modelType':modelType,'method':method,'title':title,'html':rendered}),mimetype="application/json;charset=utf-8;")
#        else:
#            rendered = render_to_string(temp,{'modelType':modelType,'form':f,'url':'./','method':'POST','title':title,'ajax':False})
#            return HttpResponse(rendered,mimetype="text/html;charset=utf-8;")
#
#    if request.method == 'POST' and int(id)==0:
#        data=request.POST.copy() # Копируем массив, ибо request - read only
#        for field in data:
#            data[field]=data[field].replace(',','.')
#        f = form(data)
#        if f.is_valid():
#            ins = f.save(commit=False)
##            f.save_m2m()
#            return redirect(ins)
#        else:
##            del form.errors['__all__']
#            return HttpResponse(json(f.errors),mimetype="application/json;charset=utf-8")
#
#    if int(id)!=0 and (request.method == 'POST' or request.method == 'PUT'):
#        if request.method == 'POST':
#            data=request.POST.copy()
#        else:
#            data=request.PUT.copy() # Копируем массив, ибо request - read only
#        print data
#        for field in data:
#            if field in ('solds','transfers'):
#                continue
#            print field,data[field]
#            data[field]=data[field].replace(',','.')
#        print model.objects.get(pk=id)
#        f = form(data,instance=model.objects.get(pk=id))
#        if f.is_valid():
#            ins = f.save()
##            f.save_m2m()
#            return redirect(ins)
#        else:
##            del form.errors['__all__']
#            return HttpResponse(json({'status':'error','message':f.errors}),mimetype="application/json;charset=utf-8")
#
#    if request.method == 'DELETE':
#        if id == 0:
#            return HttpResponse(json({'status':'error','message':'Нельзя удалять объект с id = 0'}),mimetype="application/json;charset=utf-8")
#        else:
#            model.objects.get(pk=id).delete()
#            return HttpResponse(json({'status':'deleted','id':id}),mimetype="application/json;charset=utf-8")
