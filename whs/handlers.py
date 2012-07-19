# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from whs.forms import YearMonthFilter
from whs.models import Sold, Add, Sorting

__author__ = 'bteam'
import datetime

from piston.handler import BaseHandler
from piston.utils import rc

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


class BrickHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, *args, **kwargs):
        pk = int(kwargs['pk'])
        form = YearMonthFilter(request.GET or None)
        if form.is_valid():
            data = dict([(k,v) for k,v in form.cleaned_data.items() if v is not None])
            if data.has_key('date__month'):
                b = datetime.date(year=data['date__year'],month=data['date__month'],day=1)
                e = b + relativedelta(months=1)
            else:
                b = datetime.date(year=data['date__year'],month=1,day=1)
                e = b + relativedelta(years=1)
        else:
            b = datetime.date.today().replace(day=1)
            e = b + relativedelta(months=1)

        date = dict(doc__date__range=(b,e - datetime.timedelta(1)))

        if kwargs['model'] == 'add':
            objects = Add.objects.filter(**date).filter(brick_id=pk)
            objects = objects.values_list('doc__date','amount')
        elif kwargs['model'] == 'sold':
            objects = Sold.objects.filter(**date).filter(brick_id=pk)
            objects = objects.values_list('doc__date','amount')
        elif kwargs['model'] == 't_from':
            objects = Sold.objects.filter(**date).filter(brick_from__id=pk).filter(brick_from__isnull=False)
            objects = objects.values_list('doc__date','amount')
        elif kwargs['model'] == 't_to':
            objects = Sold.objects.filter(**date).filter(brick_id=pk,brick_from__isnull=False)
            objects = objects.values_list('doc__date','amount')
        elif kwargs['model'] == 'm_from':
            date = dict([(k.replace('doc__',''),v) for k,v in date.items()])
            objects = Sorting.objects.filter(**date).filter(brick_id=pk)
            objects = objects.values_list('date','amount')
        elif kwargs['model'] == 'm_to':
            objects = Sorting.objects.filter(**date).filter(brick_id=pk)
            objects = objects.values_list('doc__date','amount')
        elif kwargs['model'] == 'm_rmv':
            objects = Removed.objects.filter(**date).filter(brick_id=pk)
            objects = objects.values_list('doc__date','amount')
        else:
            objects = []

        return objects