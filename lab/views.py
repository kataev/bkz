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


class BatchMixIn(object):
    def get_form(self,form_class):
        form = form_class(**self.get_form_kwargs())
        if self.request.GET.get('old',False):
            for n in ('pressure','flexion'):
                del form.fields[n].widget.attrs['readonly']
        return form

class BatchCreateView(BatchMixIn,BillCreateView):
    form_class=BatchForm
    model=Batch
    opers=[PressureFactory,FlexionFactory,PartFactory]

class BatchUpdateView(BatchMixIn,BillUpdateView):
    form_class=BatchForm
    model=Batch
    opers=[PressureFactory,FlexionFactory,PartFactory]
