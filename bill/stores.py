# -*- coding: utf-8 -*-
from dojango.data.modelstore import *
from whs.bill.models import *
from datetime import date

class TransferStore(Store):
    brick = StoreField('brick.__unicode__')
    amount = StoreField('amount')
    css = StoreField('brick.css')
    info = StoreField()
    parent = ReferenceField('sold')
    class Meta(object):
        objects  = Transfer.objects.all()

class SoldStore(Store):
    brick = StoreField('brick.__unicode__')
    amount = StoreField()
    price = StoreField()
    delivery = StoreField()

    css = StoreField('brick.css')
    info = StoreField()

    class Meta(object):
        objects  = Sold.objects.all()

class BillStore(Store):
    class Meta:
        stores = (SoldStore,TransferStore)


class BillsStore(Store):
    date = StoreField('date.isoformat')
    agent = StoreField('agent.__unicode__')
    agent_id = StoreField('agent.pk')
    number = StoreField()
#    css = StoreField('css')
    info = StoreField()
    money = StoreField()
    solds = StoreField()

    class Meta(object):
        objects  = Bill.objects.filter(date__month=date.today().month)


class BrickStore(Store):
    date = StoreField('doc.date_ru')
    amount = StoreField()