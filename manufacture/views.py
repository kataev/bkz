# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import get_object_or_404, render

from whs.manufacture.models import Man,Sorting
from whs.sale.forms import DateForm

def main(request):
    form = DateForm(request.GET or None)
    if form.is_valid():
        date = form.cleaned_data.get('date')
    else:
        date = datetime.date.today()
    man = Man.objects.select_related().filter(date__year=date.year,date__month=date.month)
    sorting = Sorting.objects.select_related().filter(date__year=date.year,date__month=date.month)
    return render(request,'jurnal.html',dict(man=man,sorting=sorting,form=form))