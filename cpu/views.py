# -*- coding: utf-8 -*-
from django.utils import simplejson

from django.shortcuts import render
from bkz.cpu.models import positions,line

def index(request):
    """ Главная страница """
    firing = list({'field':k,'point':v,'position':positions.get(v,'')} for k,v in line.items())
    firing.sort(key=lambda x: x['position'])
    return render(request, 'cpu/index.html', dict(firing = simplejson.dumps(firing)))