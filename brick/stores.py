# -*- coding: utf-8 -*-
from dojango.data.modelstore import *
from whs.brick.models import BrickTable
from whs.bill.models import Bill

class BricksStore(Store):
    css = StoreField( get_value=ObjectMethod('show_css') )

    mark = StoreField()
    view = StoreField()
    brick_class = StoreField()
    weight = StoreField()
    color_type = StoreField()
    
    begin = StoreField()
    plus = StoreField()
    t_from = StoreField()
    t_to = StoreField()
    sold = StoreField()
    total = StoreField()

    class Meta(object):
        objects  = BrickTable.objects.all()