# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render, redirect
from bkz.whs.pdf import pdf_render_to_response
from bkz.lab.models import *
from bkz.lab.forms import *
from django.views.generic import CreateView,UpdateView,ListView


class BatchListView(ListView):
    model = Batch

def add_print(request, id):
    doc = get_object_or_404(Batch.objects.select_related(), id=id)
    return pdf_render_to_response('lab/add.rml', {'doc': doc})

class BatchCreateView(CreateView):
    form_class=BatchForm
    model=Batch
    opers=[PartFactory,FlexionFactory,PressureFactory]
#    def get_context_data(self, **kwargs):


class BatchUpdateView(UpdateView):
    form_class=BatchForm
    model=Batch
    opers=[PartFactory,FlexionFactory,PressureFactory]
