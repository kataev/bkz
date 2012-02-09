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
    if form.is_valid():
        d = form.cleaned_data
        Bills = Bills.filter(**dict([ [x,d[x]] for x in d if d[x] ]))
    paginator = Paginator(Bills, 25) # Show 25 contacts per page

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        bills = paginator.page(page)
    except (EmptyPage, InvalidPage):
        bills = paginator.page(paginator.num_pages)
    form = BillFilter()
    return render(request,'bills.html',dict(Bills=bills,Filter=form))


def bill(request,id):
    """ Форма накладной """
    if id: doc = get_object_or_404(Bill,pk=id)
    else: doc = None

    if request.method == 'POST':
        form = BillForm(request.POST,instance=doc,)
        sold = SoldFactory(request.POST,instance=doc,prefix='sold')
        transfer = TransferFactory(request.POST,instance=doc,prefix='transfer')
        if form.is_valid() and sold.is_valid() and transfer.is_valid():
            doc = form.save()
            sold.save()
            transfer.save()
            return redirect(doc)
    else:
        form = BillForm(instance=doc)
        sold = SoldFactory(instance=doc,prefix='sold')
        transfer = TransferFactory(instance=doc,prefix='transfer')

    return render(request, 'doc.html',dict(doc=form,opers=[sold,transfer]))

