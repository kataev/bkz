# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Sum
from whs.bill.models import Bill

class BrickManager(models.Manager):
    def date(self, *args, **kwargs):
        print  args, kwargs
        bills = Bill.objects.filter(**kwargs)
#        len(bills)
        queryset = self.get_query_set()
        for b in queryset:
            b.data['sold']=bills.filter(sold__brick=b).aggregate(sold=Sum('sold__amount'))['sold']
            b.data['t_from']=bills.filter(transfer__brick=b).aggregate(t_from=Sum('transfer__amount'))['t_from']
            if b.data['sold'] > 0:
                print b.pk,b.data
        print queryset[0].data
        return queryset
