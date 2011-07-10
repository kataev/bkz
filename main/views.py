# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.views.decorators.http import require_http_methods
from cjson import encode as json
from django.db.models import Sum

import datetime
from whs.bricks.models import *
from whs.bills.models import *

from dojango.util import dojo_collector
from dojango.decorators import json_response

def main(request):
#    bills = bill.objects.latest('doc_date')[:10]

    brick_sum = bricks.objects.values('brick_class').annotate(total=Sum('total')).order_by('brick_class')
    for br in brick_sum:
        br['brick_class']=bricks.class_c[br['brick_class']][1]

    bills = []
    for b in bill.objects.filter(doc_date__gte=(datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()))):
        money=0
        for s in b.solds.all():
            money+=s.price * s.amount
        bq = {'name':unicode(b),'money':money}
        bills.append(bq)



    return render_to_response('main.html',{'brick_total':brick_sum,'bills':bills,'bricks':bricks.objects.all()},
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
    dojo_collector.add_module("dijit.form.Select")
#    dojo_collector.add_module("dijit._Widget")

#    f.fields['brick'].widget.dojo_type='whs.select.brick'
    return render_to_response('doc_add.html',{'form':f,'title':'Новая отгрузка'},
                          context_instance=RequestContext(request))


def sold_show(request,id):
    id = int(id)
    f = soldForm(instance=sold.objects.get(pk=id))
    dojo_collector.add_module("dijit.form.Form")
    dojo_collector.add_module("dijit.form.Button")
    dojo_collector.add_module("dijit.form.Select")
    return render_to_response('doc_add.html',{'form':f,'title':'','brickSelectForm':brickSelectForm()},
                          context_instance=RequestContext(request))

def brick_show(request,id):
    id = int(id)
    f = brickSelectForm(instance=bricks.objects.get(pk=id))
    dojo_collector.add_module("dijit.form.Form")
    dojo_collector.add_module("dijit.form.Button")
    dojo_collector.add_module("dijit.form.Select")
#    dojo_collector.add_module("dijit._Widget")
#    f.fields['brick'].widget.dojo_type='whs.select.brick'
    return render_to_response('doc_add.html',{'form':f,'title':''},
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
        print data
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

def form(request,modelName,id=0):
    model = {'bricks':bricks,'bill':bill,'sold':sold,'transfer':transfer}[modelName]
    form = {'bricks':brickForm,'bill':billForm,'sold':soldForm,'transfer':transferForm}[modelName]

    modelType=model.__base__.__name__

#    if modelName not in models.keys():
#        return HttpResponse(json({'status':'error','message':'DoesNotExist'}),mimetype="application/json;charset=utf-8")

    if request.method == 'GET':

        if int(id)==0:
            f=form()
            method='Post'
            url = 'form/%s/' % modelName
            if modelName in ('bricks','transfers',):
                title=u'Новый %s' % model._meta.verbose_name.lower()
            else:
                title=u'Новая %s' % model._meta.verbose_name.lower()
        else:
            url = 'form/%s/%s/' % (modelName,id)
            method='Put'
            title=u'Изменение %s № %s' % (model._meta.verbose_name_plural.lower(),id)
            try:
                f=form(instance=model.objects.get(pk=id))
            except model.DoesNotExist:
                return HttpResponse(json({'status':'error','message':'DoesNotExist'}),mimetype="application/json;charset=utf-8")
            method='Put'

        if modelName in ['solds','transfers']:
            temp=modelName+'.html'
        else:
            temp='form.html'

#        if request.is_ajax():
#            rendered = render_to_string(temp,{'form':f,'url':url,'method':method,'title':title,'ajax':True})
#            return HttpResponse(json({'modelType':modelType,'method':method,'title':title,'html':rendered}),mimetype="application/json;charset=utf-8;")
#        else:
#            rendered = render_to_string(temp,{'modelType':modelType,'form':f,'url':'./','method':'POST','title':title,'ajax':False})
#            return HttpResponse(rendered,mimetype="text/html;charset=utf-8;")
        dojo_collector.add_module("dijit.form.Form")
        dojo_collector.add_module("dijit.form.Button")
        dojo_collector.add_module("dijit.form.Select")
        dojo_collector.add_module("dojo.date")
        dojo_collector.add_module("dojo.date.locale")

        return render_to_response('doc_add.html',{'form':f,'title':title,'method':method},
                          context_instance=RequestContext(request))

    if request.method == 'POST' and int(id)==0:
        print 'POST'
        data=request.POST.copy() # Копируем массив, ибо request - read only
        for field in data:
            data[field]=data[field].replace(',','.')
        print data
        f = form(data)
        if f.is_valid():
            ins = f.save()
            return HttpResponse(json({'status':True,'id':ins.pk}),mimetype="application/json;charset=utf-8")
        else:
            return HttpResponse(json({'status':False,'message':f.errors}),mimetype="application/json;charset=utf-8")

    if int(id)!=0 and (request.method == 'POST' or request.method == 'PUT'):
        print 'PUT'
        if request.method == 'POST':
            data=request.POST.copy()
        else:
            print request.PUT
            data=request.PUT.copy() # Копируем массив, ибо request - read only
        print data
        for field in data:
            if field in ('solds','transfers'):
                continue
            data[field]=data[field].replace(',','.')
        print model.objects.get(pk=id)
        f = form(data,instance=model.objects.get(pk=id))
        if f.is_valid():
            ins = f.save()
            return HttpResponse(json({'status':True,'id':ins.pk}),mimetype="application/json;charset=utf-8")
        else:
#            del form.errors['__all__']
            return HttpResponse(json({'status':False,'message':f.errors}),mimetype="application/json;charset=utf-8")

    if request.method == 'DELETE':
        if id == 0:
            return HttpResponse(json({'status':False,'message':'Нельзя удалять объект с id = 0'}),mimetype="application/json;charset=utf-8")
        else:
            model.objects.get(pk=id).delete()
            return HttpResponse(json({'status':True,'id':id}),mimetype="application/json;charset=utf-8")


def posting(request,modelName,id):
    model = {'bricks':bricks,'bill':bill,'sold':sold,'transfer':transfer}[modelName]
    id = int(id)
    try:
        model.objects.get(pk=id).posting()
        return HttpResponse(json({'status':True,'id':id}),mimetype="application/json;charset=utf-8")
    except:
        return HttpResponse(json({'status':False,'id':id}),mimetype="application/json;charset=utf-8")