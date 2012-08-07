# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render, redirect
from bkz.whs.pdf import pdf_render_to_response
from bkz.lab.models import *
from bkz.lab.forms import *
from bkz.whs.views import BillCreateView,BillUpdateView,ListView

class BatchListView(ListView):
    model = Batch

def add_print(request, id):
    doc = get_object_or_404(Batch.objects.select_related(), id=id)
    return pdf_render_to_response('lab/add.rml', {'doc': doc})



class BatchCreateView(BillCreateView):
    form_class=BatchForm
    model=Batch
    opers=[PressureFactory,FlexionFactory,PartFactory]

class BatchUpdateView(BillUpdateView):
    form_class=BatchForm
    model=Batch
    opers=[PressureFactory,FlexionFactory,PartFactory]
    def form_valid(self, form):
        instance = form.save(commit=False)
        opers = self.get_context_data()['opers']

        for factory in opers:
            if factory.is_valid():
                a = factory.save()
        if all([f.is_valid() for f in opers]):
            instance.amount = sum([x.cleaned_data.get('amount') for x in opers[-1]])
            instance.tto = ''.join([x.cleaned_data.get('tto')+',' for x in opers[-1]])
            instance.save()
            return redirect(instance.get_absolute_url())

        return self.render_to_response(dict(form=form,opers=opers))