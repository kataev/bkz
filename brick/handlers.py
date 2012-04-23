# -*- coding: utf-8 -*-
__author__ = 'bteam'
from piston.handler import BaseHandler
from piston.utils import rc

from whs.sale.models import Sold
from whs.manufacture.models import Add,Sorted,Sorting,Removed

class BrickHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, *args, **kwargs):
        month = int(kwargs['month'])
        year = int(kwargs['year'])
        pk = int(kwargs['pk'])

        date = dict(doc__date__year=year, doc__date__month=month)

        if kwargs['model'] == 'add':
            objects = Add.objects.filter(**date).filter(brick__pk=pk)
            objects =objects.values_list('doc__date','amount')
        elif kwargs['model'] == 'sold':
            objects = Sold.objects.filter(**date).filter(brick__pk=pk)
            objects = objects.values_list('doc__date','amount')
        elif kwargs['model'] == 't_from':
            objects = Sold.objects.filter(**date).filter(brick_from__pk=pk)
            objects = objects.values_list('doc__date','amount')
        elif kwargs['model'] == 't_to':
            objects = Sold.objects.filter(**date).filter(brick__pk=pk,brick_from__isnull=False)
            objects = objects.values_list('doc__date','amount')
        elif kwargs['model'] == 'm_from':
            objects = Sorting.objects.filter(**date).filter(brick__pk=pk)
            objects = objects.values_list('date','amount')
        elif kwargs['model'] == 'm_to':
            objects = Sorted.objects.filter(**date).filter(brick__pk=pk)
            objects = objects.values_list('doc__date','amount')
        elif kwargs['model'] == 'm_rmv':
            objects = Removed.objects.filter(**date).filter(brick__pk=pk)
            objects = objects.values_list('doc__date','amount')
        else:
            objects = []

        return objects