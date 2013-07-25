# -*- coding: utf-8 -*-
from django.utils import simplejson
from operator import itemgetter

from django.shortcuts import render
from bkz.cpu.models import positions, line, target


def index(request):
    """ Главная страница """
    firing = list(
        {'field': k, 'point': v, 'position': positions.get(v, ''), 'target': target[v]} for k, v in line.items())
    firing.sort(key=itemgetter('position'))
    return render(request, 'cpu/index.html', dict(firing=simplejson.dumps(firing)))
