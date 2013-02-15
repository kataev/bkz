# -*- coding: utf-8 -*-
from django.shortcuts import render

from bkz.cpu.models import pos,line

def index(request):
    """ Главная страница """

    return render(request, 'cpu/index.html',dict(positions = pos,line=line))


