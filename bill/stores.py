# -*- coding: utf-8 -*-
from dojango.data.modelstore import *
from whs.bill.models import Bill,Sold,Transfer
from datetime import date

class TransferStore(Store):
    brick = StoreField('brick.__unicode__')
    amount = StoreField('amount')
    css = StoreField('brick.css')
    info = StoreField()

    class Meta(object):
        objects  = Transfer.objects.all()

class SoldStore(Store):
    brick = StoreField('brick.__unicode__')
    amount = StoreField()
    price = StoreField()
    delivery = StoreField()
    children = ReferenceField(get_value=ObjectMethod('bill_transfer_related.all'))
    css = StoreField('brick.css')
    info = StoreField()

    class Meta(object):
        stores = (TransferStore,)
        objects  = Sold.objects.all()

class BillStore(Store):
    date = StoreField('date.isoformat')
    agent = StoreField('agent.__unicode__')
    agent_id = StoreField('agent.pk')
    number = StoreField()
#    children = ReferenceField('bill_sold_related')
    info = StoreField()
    money = StoreField()

    class Meta(object):
        objects  = Bill.objects.filter(date__month=date.today().month)


class BrickStore(Store):
    date = StoreField('doc.date_ru')
    amount = StoreField()