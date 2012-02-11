# -*- coding: utf-8 -*-
from whs.brick.models import Brick

def bricks(request):
    Bricks = Brick.objects.all()
    return dict(Bricks=Bricks)