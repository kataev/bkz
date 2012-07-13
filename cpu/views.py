# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.serializers import serialize

from whs.cpu.models import Position,Device,pos,line

def main(request):
    """ Главная страница """


    return render(request, 'cpu.html',dict(positions = pos,line=line))


