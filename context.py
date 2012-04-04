# -*- coding: utf-8 -*-
from whs.brick.models import Brick
from django.core.urlresolvers import resolve, Resolver404

def bricks(request):
    Bricks = Brick.objects.all()
    return dict(Bricks=Bricks)

def namespace(request):
    try:
        url = resolve(request.path)
        return dict(namespace = url.namespace)
    except Resolver404:
        return dict()
