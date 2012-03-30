# -*- coding: utf-8 -*-
from whs.brick.models import Brick
from django.core.urlresolvers import resolve

def bricks(request):
    Bricks = Brick.objects.all()
    return dict(Bricks=Bricks)

def namespace(request):
    return dict(namespace = resolve(request.path).namespace)