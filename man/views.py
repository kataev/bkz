# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import get_object_or_404, render

from whs.man.models import Add,Sorting,Sorted
from whs.sale.forms import DateForm

def main(request):
    form = DateForm(request.GET or None)
    if form.is_valid():
        date = form.cleaned_data.get('date')
    else:
        date = datetime.date.today()
    man = Add.objects.select_related().filter(doc__date__year=date.year,doc__date__month=date.month)
    sorting = Sorting.objects.select_related().filter(date__year=date.year,date__month=date.month)
    opers = {}
    if len(sorting):
        for m in (Sorted,Removed):
            name = m._meta.object_name
            for o in m.objects.select_related().filter(doc__in=sorting):
                d = opers.get(o.doc_id,{})
                a = d.get(name,[])
                a.append(o)
                d[name] = a
                opers[o.doc_id] = d

        for b in sorting:
            b.opers = opers.get(b.pk,{})
    return render(request,'jurnal.html',dict(man=man,sorting=sorting,form=form))