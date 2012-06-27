# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib import messages
from django.core.urlresolvers import reverse

def main(request):
    """ Главная страница """
    return render(request, 'cpu.html')
