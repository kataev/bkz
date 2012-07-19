# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import CreateView, DeleteView
from django.core.urlresolvers import reverse

def flat_form(request,Form,pk=None,date=None):
    """ Форма  """
    if pk: model = get_object_or_404(Form._meta.model,pk=pk)
    elif date: model = get_object_or_404(Form._meta.model,date=date)
    else: model = None
    if request.method == 'POST':
        form = Form(request.POST,instance=model)
        if form.is_valid():
            model = form.save()
            if hasattr(model,'get_absolute_url'):
                return redirect(model.get_absolute_url())
    else:
        form = Form(initial=request.GET.dict() or None,instance=model)
    return render(request, 'flat-form.html',dict(form=form))