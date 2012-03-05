# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from manufacture.forms import *
from manufacture.models import *
import signals
from whs.log import construct_change_message,log_change,log_addition,log_deletion,LogEntry

def man(request,id):
    """ Форма накладной """
    if id:
        doc = get_object_or_404(Man.objects.select_related(),pk=id)
        c = ContentType.objects.get_for_model(doc)
        log = LogEntry.objects.filter(content_type=c,object_id=id)
    else: doc = None

    if request.method == 'POST':
        form = ManForm(request.POST,instance=doc,prefix='man',)
        add = AddFactory(request.POST,instance=doc,prefix='add')
        if form.is_valid():
            doc = form.save()
        if add.is_valid():
            add.save()
        if form.is_valid() and add.is_valid():
            if id:
                message = construct_change_message(form,[add])
                log_change(request,doc,message)
            else:
                log_addition(request,doc)
            return redirect('/man/%d/' % doc.pk)
    else:
        form = ManForm(instance=doc,prefix='man')
        add = AddFactory(instance=doc,prefix='add')

    return render(request, 'doc.html',dict(doc=form,opers=[add],log=log))


def srt(request,id):
    """ Форма накладной """
    if id: doc = get_object_or_404(Sorting,pk=id)
    else: doc = None
    if request.method == 'POST':
        form = SortingForm(request.POST,instance=doc,prefix='sorting')
        srted = SortedFactory(request.POST,instance=doc,prefix='sorted')
        removed = RemovedFactory(request.POST,instance=doc,prefix='removed')
        if form.is_valid():
            doc = form.save()
        if srted.is_valid():
            srted.save()
        if removed.is_valid():
            removed.save()
        if form.is_valid() and srted.is_valid() and removed.is_valid():
            return redirect('/sort/%d/' % doc.pk)
    else:
        initial = {}
        form = SortingForm(instance=doc,initial=initial,prefix='sorting')
        srted = SortedFactory(instance=doc,prefix='sorted')
        removed = RemovedFactory(instance=doc,prefix='removed')

    return render(request, 'doc.html',dict(doc=form,opers=[srted,removed]))

def inventory(request,id):
    """ Форма накладной """
    if id: doc = get_object_or_404(Inventory,pk=id)
    else: doc = None
    if request.method == 'POST':
        form = InventoryForm(request.POST,instance=doc,prefix='inventory')
        write_off = Write_offFactory(request.POST,instance=doc,prefix='write_off')

        if form.is_valid():
            doc = form.save()
        if write_off.is_valid():
            write_off.save()
        if form.is_valid() and write_off.is_valid():
            return redirect('/inventory/%d/' % doc.pk)
    else:
        initial = {}
        form = InventoryForm(instance=doc,initial=initial,prefix='inventory')
        write_off = Write_offFactory(instance=doc,prefix='write_off')

    return render(request, 'doc.html',dict(doc=form,opers=[write_off]))