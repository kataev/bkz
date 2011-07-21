# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from cjson import encode as json
from django.db.models import Sum

import datetime
from whs.bricks.models import *
from whs.bills.models import *
from whs.agents.models import *
#from whs.main.models import *
from dojango.util import dojo_collector


from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

le = [u'',u'Созданно ',u'Измененно ',u'Удалено ']

def main(request):
    brick_sum = bricks.objects.values('brick_class').annotate(total=Sum('total')).order_by('brick_class')
    for br in brick_sum:
        br['brick_class']=bricks.class_c[br['brick_class']][1]

    bills = []
    for b in bill.objects.filter(doc_date__gte=(datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()))).order_by('-doc_date'):
        money=0
        for s in b.solds.all():
            money+=s.price * s.amount
        bq = {'name':b,'money':money}
        bills.append(bq)

    bri=[]
    total = {'s':0,'tr_m':0,'tr_p':0,'t':0}

    filter = {'doc_date__gte':datetime.date(2011,07,01)}

    for br in bricks.objects.all():
        er={'brick':br}
        s = sold.objects.filter(brick=br)
        er.update(bill.objects.filter(solds__in=s,**filter).aggregate(s=Sum('solds__amount')))
        t = transfer.objects.filter(brick=br)
        er.update(bill.objects.filter(transfers__in=t,**filter).aggregate(tr_m=Sum('transfers__amount'),tr_p=Sum('solds__amount')))
        for e in er:
            if not e == 'brick' and not er[e]==None:
                total[e]+=er[e]
        total['t']+=br.total

        bri.append(er)

    return render_to_response('main.html',{'brick_total':brick_sum,'bills':bills,'bricks':bri,'total':total},
                          context_instance=RequestContext(request))


def agents(request):

    query={}
    form = agent_filter_form(request.GET)
    if form.is_valid():
        pass
    if True:
        for a in request.GET:
            if a=='name':
                query['name__contains']=form.cleaned_data[a]
            if a=='form':
                query['form']=form.cleaned_data[a]
            if a=='type':
                query['type']=form.cleaned_data[a]
            if a=='agent':
                query['address__contains']=form.cleaned_data[a]
            if a=='inn':
                query['inn__contains']=form.cleaned_data[a]
                
        paginator = Paginator(agent.objects.filter(**query), 25) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            agents = paginator.page(page)
        except TypeError,PageNotAnInteger:
            agents = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            agents = paginator.page(paginator.num_pages)

        url = {'next':'./?','prev':'./?'}
        if 'page' in request.GET:
            q = request.GET.copy()
            q['page']=int(q['page'])+1
            url['next']=q.urlencode()
            q['page']=int(q['page'])-2
            url['prev']+=q.urlencode()
        else:
            q = request.GET.copy()
            q['page']=2
            url['next']+=q.urlencode()
        print url
    dojo_collector.add_module("dijit.form.Form")
    dojo_collector.add_module("dijit.form.Button")
    return render_to_response('agents.html',{'form':form,'agents':agents},
                          context_instance=RequestContext(request))



def bills(request):
    query={}
    if request.method == 'GET':
        form = bills_filter_form(request.GET)
        if form.is_valid():
            for a in request.GET:
                if a=='brick':
                    query['solds__brick']=form.cleaned_data[a]
                if a=='data1':
                    query['doc_date_gte']=form.cleaned_data[a]
                if a=='data2':
                    query['doc_date_lte']=form.cleaned_data[a]
                if a=='agent':
                    query['agent']=form.cleaned_data[a]
                if a=='number':
                    query['number__contains']=form.cleaned_data[a]

#        bills=bill.objects.filter(**query)[:20]
        paginator = Paginator(bill.objects.filter(**query), 25) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            bills = paginator.page(page)
        except TypeError,PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            bills = paginator.page(paginator.num_pages)

        url = {'next':'./?','prev':'./?'}
        if 'page' in request.GET:
            q = request.GET.copy()
            q['page']=int(q['page'])+1
            url['next']=q.urlencode()
            q['page']=int(q['page'])-2
            url['prev']+=q.urlencode()
        else:
            q = request.GET.copy()
            q['page']=2
            url['next']+=q.urlencode()
        print url

        dojo_collector.add_module("dijit.form.Form")
        form = bills_filter_form(request.GET)
#        print 'brick',form.fields['brick']
#        form.fields['brick'].widget.dojo_type = 'whs.select.Brick'
        return render_to_response('bills.html',{'form':form,'brickform':brickForm(),'bills':bills,'url':url},
                          context_instance=RequestContext(request))





def form(request,modelName,id=0):
    try:
        model = {'bricks':bricks,'bill':bill,'sold':sold,'transfer':transfer,'agent':agent}[modelName]
        form = {'bricks':brickForm,'bill':billForm,'sold':soldForm,'transfer':transferForm,'agent':agentForm}[modelName]
    except :
        return HttpResponse('404',mimetype="application/json;charset=utf-8")


    modelType=model.__base__.__name__

    if request.method == 'GET':

        if int(id)==0:
            f=form(request.GET)
            method='POST'
            if modelName in ('bricks','transfers',):
                title=u'Новый %s' % model._meta.verbose_name.lower() #Refactor
            else:
                title=u'Новая %s' % model._meta.verbose_name.lower()
        else:
            method='Put'
            title=u'Изменение %s № %s' % (model._meta.verbose_name_plural.lower(),id)
            try:
                instance=model.objects.get(pk=id)
                f=form(instance=instance)
            except model.DoesNotExist:
                return HttpResponse(json({'status':'error','message':'DoesNotExist'}),mimetype="application/json;charset=utf-8")

        dojo_collector.add_module("dijit.form.Form")
        dojo_collector.add_module("dijit.form.Button")
        dojo_collector.add_module("dijit.form.Select")
        dojo_collector.add_module("dijit.form.DateTextBox")
        dojo_collector.add_module("dijit.form.NumberSpinner")
        dojo_collector.add_module("dojo.date")
        dojo_collector.add_module("dojo.date.locale")
#        dojo_collector.add_module("dojo.parser")

        history = []
#        if id != 0:
#            for h in LogEntry.objects.filter(content_type=ContentType.objects.get_for_model(model).id,object_id=id):
#                history.append({'action_time':h.action_time,'change_message':le[h.action_flag]+h.change_message})

        if modelName=='agent':
            return render_to_response('doc_add.html',{'form':f,'title':title,'method':method,'history':history},
                          context_instance=RequestContext(request))

        if modelType=='doc':
            if id!=0:
                f.fields['solds'].queryset=f.instance.solds.all()
                f.fields['transfers'].queryset=f.instance.transfers.all()
            return render_to_response('doc_add.html',{'form':f,'title':title,'method':method,'history':history},
                          context_instance=RequestContext(request))
        if modelType=='oper':
            if int(id)==0:
                brick = brickForm()
            else:
                brick = brickForm(instance=model.objects.get(pk=id).brick)
            return render_to_response('oper_add.html',{'form':f,'title':title,'method':method,'history':history,'brickform':brick},
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
            LogEntry.objects.log_action(
                user_id         = 1,
                content_type_id = ContentType.objects.get_for_model(ins).pk,
                object_id       = ins.pk,
                object_repr     = force_unicode(ins),
                action_flag     = ADDITION
                )

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
        i=model.objects.get(pk=id)
        f = form(data,instance=i)
        if f.is_valid():
            ins = f.save()
            mes = u''
            print f.changed_data
            if len(f.changed_data) > 0:
                for field in f.changed_data:
                    mes+= f.fields[field].label.lower()
                    mes+=','
                print 'mess %s' % mes
            LogEntry.objects.log_action(
                user_id         = 1,
                content_type_id = ContentType.objects.get_for_model(ins).pk,
                object_id       = ins.pk,
                object_repr     = force_unicode(ins) + mes[:-1],
                action_flag     = CHANGE,
                change_message  = mes[:-1]
                )

            return HttpResponse(json({'status':True,'id':ins.pk}),mimetype="application/json;charset=utf-8")
        else:
#            del form.errors['__all__']
            return HttpResponse(json({'status':False,'message':f.errors}),mimetype="application/json;charset=utf-8")

    if request.method == 'DELETE':
        if id == 0:
            return HttpResponse(json({'status':False,'message':'Нельзя удалять объект с id = 0'}),mimetype="application/json;charset=utf-8")
        else:
            model.objects.get(pk=id).delete()
            LogEntry.objects.log_action(
                user_id         = 1,
                content_type_id = ContentType.objects.get_for_model(ins).pk,
                object_id       = ins.pk,
                object_repr     = force_unicode(ins),
                action_flag     = DELETION
                )
            return HttpResponse(json({'status':True,'id':id}),mimetype="application/json;charset=utf-8")


def posting(request,modelName,id):
    try:
        model = {'bricks':bricks,'bill':bill,'sold':sold,'transfer':transfer}[modelName]
    except :
        return HttpResponse('404',mimetype="application/json;charset=utf-8")
    id = int(id)
    try:
        ins = model.objects.get(pk=id)
        ins.posting()
        LogEntry.objects.log_action(
                user_id         = 1,
                content_type_id = ContentType.objects.get_for_model(ins).pk,
                object_id       = ins.pk,
                object_repr     = force_unicode(ins)+u' опубликован',
                action_flag     = CHANGE
                )
        return HttpResponse(json({'status':True,'id':id}),mimetype="application/json;charset=utf-8")
    except:
        return HttpResponse(json({'status':False,'id':id}),mimetype="application/json;charset=utf-8")