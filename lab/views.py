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
        self.seonr = SEONR.objects.filter(color=self.object.color).latest('date')
        self.efflorescence = Efflorescence.objects.filter().latest('date')
        self.heatconduction = HeatConduction.objects.filter(width=self.object.width).latest('date')
        self.frost_resistance = FrostResistance.objects.filter(color=self.object.color).latest('date')
        self.water_absorption = WaterAbsorption.objects.filter().latest('date')
        self.object.save()
        return redirect(self.get_success_url())

class BatchUpdateView(UpdateView):
    form_class=BatchForm
    model=Batch
    def form_valid(self, form):
        context = self.get_context_data(form=form)
        self.object = form.save(commit=False)
        if self.parts.is_valid():
            self.parts.save(commit=False)
            for part in self.parts.initial_forms:
                if part.rows.is_valid():
                    part.instance.amount = sum([r.instance.out for r in part.rows.initial_forms])
                    part.instance.tto = ','.join([r.instance.tto for r in part.rows.initial_forms])
                    part.instance.save()
                    print part.instance.pk
                    print [p.pk for p in part.rows.save()]
            self.parts.save()
            self.object.amount = sum([r.instance.amount for r in self.parts.initial_forms])
            self.object.tto = ','.join([r.instance.tto for r in self.parts.initial_forms])
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
def batch_print(request, pk):
    batch = get_object_or_404(Batch.objects.select_related(), pk=pk)
    return render_to_response('webodt/akt-out.odt',{'batch':batch},format='pdf',inline=True)


def batch_tests(request,pk):
    batch = get_object_or_404(Batch.objects.select_related(), pk=pk)
    flexion = FlexionFactory(request.POST or None, instance=batch)
    pressure = PressureFactory(request.POST or None, instance=batch)
    if request.method == 'POST' and flexion.is_valid() and pressure.is_valid():
        flexion.save()
        pressure.save()
        return batch.get_tests_url()
    return render(request,'lab/batch-tests.html',{'flexion':flexion,'pressure':pressure,'batch':batch})