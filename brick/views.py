# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect, render
from whs.brick.models import make_css,make_label

def flat_form(request,Form,id):
    """ Форма  """
#    id = args[0]
    if id: instance = get_object_or_404(Form._meta.model,pk=id)
    else: instance = None
    if request.method == 'POST':
        form = Form(request.POST,instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.label = make_label(instance)
            instance.css = make_css(instance)
            instance.save()
            return redirect(instance.get_absolute_url()+'?success=True')
    else:
        form = Form(instance=instance)
    return render(request, 'flat-form.html',dict(form=form,success=request.GET.get('success',False)))