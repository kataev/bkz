# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from bkz.whs.views import BillCreateView
from django.views.generic import UpdateView

from bkz.lab.models import *
from bkz.lab.forms import *

class BatchCreateView(BillCreateView):
    form_class=BatchForm
    model=Batch
    opers=[PressureFactory,FlexionFactory,PartFactory]
    def form_valid(self, form):
        self.object = form.save(commit=False)
        width = self.object.width
        if width == 0.8:
            width = 1.0
        self.object.seonr = SEONR.objects.filter(color=self.object.color).latest('date')
        self.object.efflorescence = Efflorescence.objects.filter().latest('date')
        self.object.heatconduction = HeatConduction.objects.filter(width=width).latest('date')
        self.object.frost_resistance = FrostResistance.objects.filter(color=self.object.color).latest('date')
        self.object.water_absorption = WaterAbsorption.objects.filter().latest('date')
        self.object.save()
        return redirect(self.get_success_url())

class BatchUpdateView(UpdateView):
    form_class=BatchForm
    model=Batch
    def form_valid(self, form):
        context = self.get_context_data(form=form)
        self.object = form.save(commit=False)
        for part in self.parts:
            if part.is_valid() and part.has_changed():
                part.save()
            if part.rows.is_valid() and part.instance.pk:
                part.rows.save()
        self.object.amount = sum([r.instance.out or 0 for r in self.parts])
        self.object.tto = ','.join([r.instance.tto for r in self.parts])
        self.object.save()
        if all([p.is_valid() and p.rows.is_valid() for p in self.parts]):
            messages.add_message(self.request, messages.SUCCESS, u'Партия сохранена успешно!')
            return redirect(self.get_success_url())
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        self.parts = PartFactory(self.request.POST or None, instance=self.object)
        for part in self.parts:
            part.rows = RowFactory(self.request.POST or None, instance=part.instance,prefix=part.prefix+'-row')
        context['parts'] = self.parts
        return context

def index(request):
    batch_list = Batch.objects.all()
    raw_list = Raw.objects.all()
    return render(request,'lab/index.html',dict(batch_list=batch_list,raw_list=raw_list))


from webodt.shortcuts import render_to_response
def batch_print_akt(request, pk):
    batch = get_object_or_404(Batch.objects.select_related(), pk=pk)
    return render_to_response('webodt/akt-out.odt',{'batch':batch},format='pdf',inline=True)


def batch_print_doc(request, pk):
    batch = get_object_or_404(Batch.objects.select_related(), pk=pk)
    return render_to_response('webodt/document-the-quality-of.odt',{'batch':batch},format='pdf',inline=True)


def batch_tests(request,pk):
    batch = get_object_or_404(Batch.objects.select_related(), pk=pk)
    initial = [{'row':2},{'row':2},{'row':8},{'row':8},{'row':16},{'row':16}]
    flexion = FlexionFactory(request.POST or None, instance=batch,initial=initial)
    pressure = PressureFactory(request.POST or None, instance=batch,initial=initial)
    form = BatchTestsForm(request.POST or None,instance=batch)
    if request.method == 'POST':
        if form.is_valid():
            batch = form.save()
            messages.add_message(request, messages.SUCCESS, u'Характеристики сохранены!')
        if flexion.is_valid():
            flexion.save()
            fle = flexion.get_value
            messages.add_message(request, messages.SUCCESS, u'Исптания на изгиб сохранены!')
        if pressure.is_valid():
            pressure.save()
            pre = pressure.get_value
            messages.add_message(request, messages.SUCCESS, u'Исптания на сжатие сохранены!')
        if pressure.is_valid() and flexion.is_valid():
            if pre and fle:
                batch.mark = min((fle['mark'],pre['mark']))
                batch.pressure = pre['avgn']
                batch.flexion = fle['avgn']
                batch.save()
                messages.add_message(request, messages.SUCCESS, u'Марка определена!')
                return redirect(batch.get_tests_url())
            else:
                messages.add_message(request, messages.WARNING, u'Не хватает данных для определения марки!')
    tests = [pressure,flexion]
    return render(request,'lab/batch-tests.html',{'tests':tests,'batch':batch,'form':form})