# -*- coding: utf-8 -*-
from dojango.data.modelstore import *
from whs.brick.models import BrickTable
from whs.bill.models import Bill

class BrickStore(Store):
    name = StoreField( get_value=ObjectMethod('__unicode__') )
    css = StoreField( get_value=ObjectMethod('show_css') )

    mark = StoreField()
    view = StoreField()

    begin = StoreField()
    t_from = StoreField()
    t_to = StoreField()
    sold = StoreField()
    total = StoreField()

    class Meta(object):
        objects  = BrickTable.objects.all()
        label    = 'name'

if __name__ == '__main__':

    store = BrickStore()
#    print store.to_python()