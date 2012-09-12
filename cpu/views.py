# -*- coding: utf-8 -*-
from django.shortcuts import render

from bkz.cpu.models import pos,line

def main(request):
    """ Главная страница """
    return render(request, 'cpu/cpu.html',dict(positions = pos,line=line))


