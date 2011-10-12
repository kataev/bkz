# -*- coding: utf-8 -*-
from dojango.data.modelstore import *
from whs.brick.models import BrickTable,Brick

class BrickSelectStore(Store):
    css = StoreField()
    total = StoreField()
    label = StoreField()

    class Meta(object):
        objects  = Brick.objects.all()


class BricksStore(BrickSelectStore):
    begin = StoreField()
    add = StoreField()
    t_from = StoreField()
    t_to = StoreField()
    sold = StoreField()

    class Meta(object):
        objects  = BrickTable.objects.all()


