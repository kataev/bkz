# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render, redirect
from bkz.lab.models import *
from bkz.lab.forms import *
from bkz.whs.views import BillCreateView,BillUpdateView
from django.views.generic import UpdateView, CreateView, ListView

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
        self.object = form.save()
        parts = PartFactory(self.request.POST or None, instance=self.object)
        error = False
        print 'test'
        if parts.is_valid():
            parts.save()
            for part in parts:
                part.rows = RowFactory(self.request.POST or None, instance=part.instance,prefix=part.prefix+'-row')
                if part.rows.is_valid():
                     part.rows.save()
                else:
                    error = True
                    print 'rows not valid',part.rows.errors
        else:
            print 'parts not valid',parts.errors
            return self.render_to_response(self.get_context_data(form=form))
        if error:
            return self.render_to_response(dict(form=form,parts=parts))
        else:
            return redirect(self.get_success_url()+'?success=True')

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        if not context.has_key('parts'):
            context['parts'] = PartFactory(self.request.POST or None, instance=self.object)
            for part in context['parts']:
                part.rows = RowFactory(self.request.POST or None, instance=part.instance,prefix=part.prefix+'-row')
                part.rows.clean()
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