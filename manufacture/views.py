# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from manufacture.forms import *
from manufacture.models import *
import signals

def man(request,id):
    """ Форма накладной """
    if id: doc = get_object_or_404(Man.objects.select_related(),pk=id)
    else: doc = None

    if request.method == 'POST':
        form = ManForm(request.POST,instance=doc,prefix='man',)
        add = AddFactory(request.POST,instance=doc,prefix='add')
        if form.is_valid() and add.is_valid():
            doc = form.save()
            add.save()
            return redirect(doc)
    else:
        form = ManForm(instance=doc,prefix='man')
        add = AddFactory(instance=doc,prefix='add')

    return render(request, 'doc.html',dict(doc=form,opers=[add]))


def srt(request,id):
    """ Форма накладной """
    if id: doc = get_object_or_404(Sorted,pk=id)
    else: doc = None
    if request.method == 'POST':
        form = SortedForm(request.POST,instance=doc,prefix='sorting')
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
        form = SortedForm(instance=doc,initial=initial,prefix='sorting')
        srted = SortedFactory(instance=doc,prefix='sorted')
        removed = RemovedFactory(instance=doc,prefix='removed')

    return render(request, 'doc.html',dict(doc=form,opers=[srted,removed]))