# -*- coding: utf-8 -*-
import datetime
from django.db.models import Max
from django.shortcuts import render, get_object_or_404,redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, UpdateView

from error_pages.http import Http403,Http401
from bill.models import Bill

from whs.manufacture.forms import *
from whs.bill.forms import *
from whs.log import construct_change_message,log_change,log_addition,log_deletion
from django.contrib.auth.decorators import login_required, permission_required

@require_http_methods(["GET",])
def main(request):
    """ Главная страница """
    return render(request, 'index.html')

def journal(request):
    form = DateForm(request.GET or None)
    if form.is_valid(): date = form.cleaned_data.get('date')
    else: date = datetime.date.today()

    Jounal = list(Bill.objects.select_related().filter(date=date))+list(Man.objects.select_related().filter(date=date))

    return render(request,'journal.html',dict(Journal=Jounal,date=form))

def flat_form(request,Form,id):
    """ Форма  """
#    id = args[0]
    if id: model = get_object_or_404(Form._meta.model,pk=id)
    else: model = None
    if request.method == 'POST':
        form = Form(request.POST,instance=model)
        if form.is_valid():
            model = form.save()
            if id:
                message = construct_change_message(form,[])
                log_change(request,model,message)
            else:
                log_addition(request,model)
            return redirect(model)
    else:
        form = Form(instance=model)
    return render(request, 'flat-form.html',dict(form=form))


def stats(request):
    return render(request,'stats.html',dict(charts=[1,2,3,4]))


class CreateView(CreateView):
    template_name = 'doc.html'

    def form_valid(self, form):
        instance = form.save()
        return redirect(instance.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        if not self.request.user.has_perm('%s.add_%s' % (self.model._meta.app_label,self.model._meta.module_name)):
            raise Http403
        return context


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
            return redirect(instance.get_absolute_url())

        return self.render_to_response(dict(form=form,opers=opers))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)

        instance = self.object
        context['opers'] = []
        if self.request.POST:
            if not self.request.user.has_perm('%s.change_%s' % (self.model._meta.app_label,self.model._meta.module_name)):
                raise Http403
            for factory in self.opers:
                context['opers'].append(factory(self.request.POST,instance=instance,prefix=factory.form.Meta.name))
        else:
            if not self.request.user.has_perm('%s.view_%s' % (self.model._meta.app_label,self.model._meta.module_name)):
                raise Http403
            for factory in self.opers:
                context['opers'].append(factory(instance=instance,prefix=factory.form.Meta.name))
        return context