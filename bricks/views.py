# -*- coding: utf-8 -*-
from django.http import HttpResponse
from whs.bricks.models import BrickStore

def store(request):
    return HttpResponse(BrickStore().to_json())