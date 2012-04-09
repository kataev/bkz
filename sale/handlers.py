# -*- coding: utf-8 -*-
__author__ = 'bteam'
import datetime

from piston.handler import BaseHandler
from piston.utils import rc

from whs.sale.forms import YearMonthFilter
from whs.sale.models import Transfer,Sold
from whs.brick.constants import color_c,weight_c,view_c,mark_c

class TransferMarkHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, *args, **kwargs):
        data = {}
        form = YearMonthFilter(request.GET or None)
        if form.is_valid():
            data = dict([ ('doc__'+k,v) for k,v in form.cleaned_data.items() if v])
        else:
            date = datetime.date.today()
            data = dict(doc__date__year=date.year,doc__date__month=date.month)

        print data
        transfers = {}
        for t in Transfer.objects.filter(**data):
            fr = transfers.get(t.brick_from.mark,{})
            fr[t.brick_to.mark] = fr.get(t.brick_to.mark,0) + t.amount
            transfers[t.brick_from.mark] = fr
        l = []
        for f in transfers:
            for t in transfers[f]:
                l.append(dict(f=f,t=t,v=transfers[f][t]))

        return l

class TotalHandler(BaseHandler):
    allowed_methods = ('GET',)
    def read(self, request, *args, **kwargs):
        data = {}
        form = YearMonthFilter(request.GET or None)
        if form.is_valid():
            data = dict([ ('doc__'+k,v) for k,v in form.cleaned_data.items() if v])
        else:
            date = datetime.date.today()
            data = dict(doc__date__year=date.year,doc__date__month=date.month)

        transfers = {}
        for s in Sold.objects.filter(**data).values('brick__view','brick__weight','brick__mark','brick__color','amount'):
            for k,v in s.items:
                pass
