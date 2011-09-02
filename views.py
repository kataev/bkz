# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from dojango.util import dojo_collector

def main(request):
    return render_to_response('main/main.html')