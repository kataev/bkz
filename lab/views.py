# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render, redirect
from bkz.lab.models import *
from bkz.lab.forms import *
from bkz.whs.views import BillCreateView,BillUpdateView

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

class BatchUpdateView(BillUpdateView):
    form_class=BatchForm
    model=Batch
    opers=[PressureFactory,FlexionFactory,PartFactory]
    redirect = {
        'redirect':'whs:Brick-list'
    }
    def form_valid(self, form):
        instance = form.save(commit=False)
        opers = self.get_context_data()['opers']
        for factory in opers.values():
            if factory.is_valid():
                a = factory.save()
        if all([f.is_valid() for f in opers.values()]):
            instance.amount = sum([x.cleaned_data.get('amount',0) for x in opers['part_set']])
            instance.tto = ','.join([x.cleaned_data.get('tto','') for x in opers['part_set']])
            instance.save()
            return redirect(self.get_success_url())
        return self.render_to_response(dict(form=form,opers=opers))

    def get_success_url(self):
        for k in filter(lambda x:'redirect' in x,self.request.POST.keys()):
            return self.redirect[k]
        else:
            return super(BatchUpdateView,self).get_success_url()


def index(request):
    batch_list = Batch.objects.all()
    raw_list = Raw.objects.all()
    return render(request,'lab/index.html',dict(batch_list=batch_list,raw_list=raw_list))


from webodt.shortcuts import render_to_response
def batch_print(request, pk):
    batch = get_object_or_404(Batch.objects.select_related(), pk=pk)
    return render_to_response('webodt/akt-out.odt',{'batch':batch},format='pdf',inline=True)
