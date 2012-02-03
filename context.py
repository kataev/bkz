# -*- coding: utf-8 -*-
from whs.brick.models import Brick

def bricks(request):
    return dict(Bricks=Brick.objects.all())