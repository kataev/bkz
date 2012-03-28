# -*- coding: utf-8 -*-
__author__ = 'bteam'
from piston.handler import BaseHandler
from piston.utils import rc

from whs.bill.models import Sold,Transfer
from whs.manufacture.models import Add,Sorted,Sorting,Removed

class BrickHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, *args, **kwargs):
        month = int(kwargs['month'])
        year = int(kwargs['year'])
        pk = int(kwargs['pk'])

        if kwargs['model'] == 'add':
            objects = Add.objects.filter(doc__date__year=year, doc__date__month=month, brick__pk=pk)
            objects =objects.values_list('doc__date','amount')
        elif kwargs['model'] == 'sold':
            objects = Sold.objects.filter(doc__date__year=year, doc__date__month=month, brick__pk=pk)
            objects =objects.values_list('doc__date','amount')
        elif kwargs['model'] == 't_from':
            objects = Transfer.objects.filter(doc__date__year=year, doc__date__month=month, brick_from__pk=pk)
            objects =objects.values_list('doc__date','amount')
        elif kwargs['model'] == 't_to':
            objects = Transfer.objects.filter(doc__date__year=year, doc__date__month=month, brick_to__pk=pk)
            objects =objects.values_list('doc__date','amount')
        elif kwargs['model'] == 'm_from':
            objects = Sorting.objects.filter(date__year=year, date__month=month, brick__pk=pk)
            objects =objects.values_list('date','amount')
        elif kwargs['model'] == 'm_to':
            objects = Sorted.objects.filter(doc__date__year=year, doc__date__month=month, brick__pk=pk)
            objects =objects.values_list('doc__date','amount')
        elif kwargs['model'] == 'm_rmv':
            objects = Removed.objects.filter(doc__date__year=year, doc__date__month=month, brick__pk=pk)
            objects =objects.values_list('doc__date','amount')
        else:
            objects = []


        return objects