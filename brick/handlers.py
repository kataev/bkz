# -*- coding: utf-8 -*-
__author__ = 'bteam'
import datetime
from dateutil.relativedelta import relativedelta

from piston.handler import BaseHandler
from piston.utils import rc

from whs.sale.models import Sold
from whs.sale.forms import YearMonthFilter
from whs.man.models import Add,Sorted,Sorting

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
            objects = Sorted.objects.filter(**date).filter(brick_id=pk)
            objects = objects.values_list('doc__date','amount')
        elif kwargs['model'] == 'm_rmv':
            objects = Removed.objects.filter(**date).filter(brick_id=pk)
            objects = objects.values_list('doc__date','amount')
        else:
            objects = []

        return objects