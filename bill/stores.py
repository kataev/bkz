# -*- coding: utf-8 -*-
from dojango.data.modelstore import *
from whs.bill.models import Bill,Sold,Transfer
from datetime import date

class TransferStore(Store):
    brick = StoreField('brick.__unicode__')
    amount = StoreField()

    class Meta(object):
        objects  = Transfer.objects.all()

class SoldStore(Store):
    brick = StoreField('brick.__unicode__')
    amount = StoreField()
    children = ReferenceField(get_value=ObjectMethod('get_transfer'))
    
    class Meta(object):
        objects  = Sold.objects.all()

class BillStore(Store):
    date = StoreField( get_value=ObjectMethod('str_date') )
    agent = StoreField( get_value=ObjectMethod('agent_unicode') )
    children = ReferenceField(model_field='sold')

    class Meta(object):
        objects  = Bill.objects.filter(date__month=date.today().month)


class BillSoldStore(Store):

    class Meta(object):
        stores = (BillStore,SoldStore,TransferStore)