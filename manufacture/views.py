# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import get_object_or_404, render

from whs.manufacture.models import Man,Sorting

def main(request):
    date = datetime.date.today()
    man = Man.objects.select_related().filter(date__year=date.year,date__month=date.month)
    sorting = Sorting.objects.select_related().filter(date__year=date.year,date__month=date.month)
    return render(request,'jurnal.html',dict(man=man,sorting=sorting))