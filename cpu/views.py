# -*- coding: utf-8 -*-
import simplejson

from django.shortcuts import render
from bkz.cpu.models import positions,line

def index(request):
    """ Главная страница """
    return render(request, 'cpu/index.html',dict(positions = simplejson.dumps(positions),line=simplejson.dumps(line)))


