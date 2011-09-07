# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from dojango.util import dojo_collector

def form(request,id):
    id = int(id)
    return render_to_response('brick.html',{'id':id})