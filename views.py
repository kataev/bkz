# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib import messages
from django.core.urlresolvers import reverse

from bkz.brick.templatetags.class_name import class_name

def index(request):
    """ Главная страница """
    return render(request, 'index.html')

def help(request):
    """ Страница помощи """
    return render(request, 'help.html')


def flat_form(request,Form,id=None,date=None):
    """ Форма  """
#    id = args[0]
    if id: model = get_object_or_404(Form._meta.model,pk=id)
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


def stats(request):
    return render(request,'stats.html',dict(charts=[1,2,3,4]))

def price(request):
    return render(request,'price.html')


class DeleteView(DeleteView):
    template_name = 'delete.html'
    def get_success_url(self):
        return reverse('%s:main' % self.object._meta.app_label)

class CreateView(CreateView):
    template_name = 'doc.html'

    def form_valid(self, form):
        instance = form.save()
        return redirect(instance.get_absolute_url())

class UpdateView(UpdateView):
    template_name = 'doc.html'
    opers = []

    def form_valid(self, form):
        instance = form.save()
        opers = self.get_context_data()['opers']

        for factory in opers:
            if factory.is_valid():
                factory.save()
        if all([f.is_valid() for f in opers]):
            messages.success(self.request,'Всё ок')
            return redirect(instance.get_absolute_url())

        return self.render_to_response(dict(form=form,opers=opers))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)

        instance = self.object
        context['opers'] = []
        if self.request.POST:
            for factory in self.opers:
                context['opers'].append(factory(self.request.POST,instance=instance,prefix=class_name(factory.form)))
        else:
            for factory in self.opers:
                context['opers'].append(factory(instance=instance,prefix=class_name(factory.form),queryset=factory.model.objects.select_related('brick','brick_from')))
        return context