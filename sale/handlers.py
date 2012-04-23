# -*- coding: utf-8 -*-
__author__ = 'bteam'
import datetime

from piston.handler import BaseHandler
from piston.utils import rc

from whs.sale.forms import YearMonthFilter
from whs.sale.models import Sold
from django.db.models import Sum

class TransferMarkHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, *args, **kwargs):
        form = YearMonthFilter(request.GET or None)
        if form.is_valid():
            data = Sold.objects.all()
        else:
            date = datetime.date.today()
            data = Sold.objects.filter(doc__date__year=date.year,doc__date__month=date.month,brick_from__isnull=False)
        data = data.values('brick__view','brick__weight','brick__mark','brick__color').annotate(Sum('amount'))
        return data

class TotalHandler(BaseHandler):
    allowed_methods = ('GET',)
    def read(self, request, *args, **kwargs):
        form = YearMonthFilter(request.GET or None)
        if form.is_valid():
            data = Sold.objects.all()
        else:
            date = datetime.date.today()
            data = Sold.objects.filter(doc__date__year=date.year,doc__date__month=date.month)
        data = data.values('brick__view','brick__weight','brick__mark','brick__color').annotate(Sum('amount'))
        return data