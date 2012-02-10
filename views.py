# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404,redirect
from django.views.decorators.http import require_http_methods
from django.forms.models import inlineformset_factory
from whs.brick.models import Brick
from whs.brick.forms import BrickForm
from whs.bill.forms import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage

@require_http_methods(["GET",])
def main(request):
    """ Главная страница """
    return render(request, 'index.html',dict(Bricks=Brick.objects.all()))


def form(request):
    """ Форма """
    if request.method == 'POST':
        form = SoldForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        BillFormSet = inlineformset_factory(Bill,Sold)
        b = Sold.objects.get(pk=1)
        form = BillFormSet(instance=b)
    return render(request, 'test.html',dict(form=form))

def bills(request):
    Bills = Bill.objects.all()
    form = BillFilter(request.GET)
    print form['brick'].value()
    if form.is_valid():
        d = form.cleaned_data
        d = dict([ [x,d[x]] for x in d if d[x]])
        if 'brick' in d.keys():
            d['bill_sold_related__brick'] = d['brick']
            del d['brick']
        Bills = Bills.filter(**d)
    paginator = Paginator(Bills, 20) # Show 25 contacts per page

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        bills = paginator.page(page)
    except (EmptyPage, InvalidPage):
        bills = paginator.page(paginator.num_pages)
    form = BillFilter()
    total = reduce(lambda memo,b: memo+b.money,bills.object_list,0)
    return render(request,'bills.html',dict(Bills=bills,Filter=form,total=total))


def bill(request,id):
    """ Форма накладной """
    if id: doc = get_object_or_404(Bill.objects.select_related(),pk=id)
    else: doc = None
    print request.POST
    if request.method == 'POST':
        form = BillForm(request.POST,instance=doc,prefix='bill')
        sold = SoldFactory(request.POST,instance=doc,prefix='sold')
        transfer = TransferFactory(request.POST,instance=doc,prefix='transfer')
        if form.is_valid() and sold.is_valid() and transfer.is_valid():
            doc = form.save()
            sold.save()
            transfer.save()
            return redirect(doc)
    else:
        form = BillForm(instance=doc,prefix='bill')
        sold = SoldFactory(instance=doc,prefix='sold')
        transfer = TransferFactory(instance=doc,prefix='transfer')

    return render(request, 'doc.html',dict(doc=form,opers=[sold,transfer]))

def brick(request,id):
    """ Форма  """
    if id: brick = get_object_or_404(Brick,pk=id)
    else: brick = None
    if request.method == 'POST':
        form = BrickForm(request.POST,instance=brick)
        if form.is_valid():
            brick = form.save()
            return redirect(brick)
    else:
        form = BrickForm(instance=brick)

    return render(request, 'brick.html',dict(form=form))