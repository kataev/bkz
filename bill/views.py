# -*- coding: utf-8 -*-
import datetime

from exceptions import ValueError
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Max
from django.http import QueryDict
from django.shortcuts import get_object_or_404, redirect, render

from whs.bill.forms import BillForm, SoldFactory, TransferFactory, BillFilter
from whs.bill.models import Bill
from whs.bill.pdf import pdf_render_to_response
import whs.bill.signals
from whs.log import construct_change_message,log_change,log_addition,log_deletion,ContentType,LogEntry

__author__ = 'bteam'

def bill(request,id):
    """ Форма накладной """
    if id:
        doc = get_object_or_404(Bill,pk=id)
        c = ContentType.objects.get_for_model(doc)
        log = LogEntry.objects.filter(content_type=c,object_id=id)[:5]
    else:
        doc = None
    if request.method == 'POST':
        form = BillForm(request.POST,instance=doc,prefix='bill')
        sold = SoldFactory(request.POST,instance=doc,prefix='sold')
        transfer = TransferFactory(request.POST,instance=doc,prefix='transfer')
        if form.is_valid():
            doc = form.save()
        if sold.is_valid():
            sold.save()
        if transfer.is_valid():
            transfer.save()
        if form.is_valid() and sold.is_valid() and transfer.is_valid():
            if id:
                message = construct_change_message(form,[sold,transfer])
                log_change(request,doc,message)
            else:
                log_addition(request,doc)
            return redirect('/bill/%d/' % doc.pk)
    else:
        initial = {}
        if not id:
            initial = Bill.objects.filter(date__year=datetime.date.today().year).aggregate(number=Max('number'))
            initial['number'] = (initial.get('number') or 0) + 1
        form = BillForm(instance=doc,prefix='bill',initial=initial)
        sold = SoldFactory(instance=doc,prefix='sold')
        transfer = TransferFactory(instance=doc,prefix='transfer')

    return render(request, 'doc.html',dict(doc=form,opers=[sold,transfer],log=log))

def bills(request):
    Bills = Bill.objects.select_related().all()
    form = BillFilter(request.GET or None)
    order = request.GET.get('order')
    if order in map(lambda x: x.name,Bill._meta.fields):
        Bills = Bills.order_by(order)

    if form.is_valid() and request.GET:
        d = form.cleaned_data
        d = dict([ [x,d[x]] for x in d if d[x]])
        if 'brick' in d.keys():
            d['bill_sold_related__brick'] = d['brick']
            del d['brick']
        Bills = Bills.filter(**d)
    paginator = Paginator(Bills, 20)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        bills = paginator.page(page)
    except (EmptyPage, InvalidPage):
        bills = paginator.page(paginator.num_pages)
    money = 0# reduce(lambda memo,b: memo+b.money,bills.object_list,0)
    total = 0#reduce(lambda memo,b: memo+b.total,bills.object_list,0)

    url = QueryDict('',mutable=True)
    get = request.GET.copy()
    get = dict([ [x,get[x]] for x in get if get[x]])
    if get.has_key('page'): del get['page']
    url.update(get)
    return render(request,'bills.html',dict(Bills=bills,Filter=form,total=total,money=money,url=url.urlencode()))

def bill_print(request,id):
    doc = get_object_or_404(Bill.objects.select_related(),pk=id)
    return pdf_render_to_response('torg-12.rml',{'doc':doc})