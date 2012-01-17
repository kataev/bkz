# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404,redirect,Http404
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET",])
def main(request):
    """ Главная страница """
    return render(request, 'index.html',)
