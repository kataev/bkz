# -*- coding: utf-8 -*-
__author__ = 'bteam'
import datetime

from piston.handler import BaseHandler
from piston.utils import rc

from bkz.sale.forms import YearMonthFilter
from bkz.sale.models import Sold
from django.db.models import Sum

class TransferMarkHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, *args, **kwargs):
        form = YearMonthFilter(request.GET or None)
        queryset = Sold.objects.filter(brick_from__isnull=False)
        if form.is_valid():

            queryset = queryset.filter(**dict([('doc__%s' % k,v) for k,v in form.cleaned_data.items() if v]))
        else:
            date = datetime.date.today()
            queryset = queryset.filter(doc__date__year=date.year,doc__date__month=date.month)
        print queryset
        queryset = queryset.values('brick__mark','brick_from__mark').annotate(Sum('amount'))

        return queryset

class TotalHandler(BaseHandler):
    allowed_methods = ('GET',)
    def read(self, request, *args, **kwargs):
        form = YearMonthFilter(request.GET or None)
        queryset = Sold.objects.all()
        if form.is_valid():
            queryset = queryset.filter(**dict([('doc__%s' % k,v) for k,v in form.cleaned_data.items() if v]))
        else:
            date = datetime.date.today()
            queryset = Sold.objects.filter(doc__date__year=date.year,doc__date__month=date.month)
        queryset = queryset.values('brick__view','brick__weight','brick__mark','brick__color').annotate(Sum('amount'))
        return queryset