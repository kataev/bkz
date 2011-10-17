# -*- coding: utf-8 -*-
__author__ = 'bteam'
from stores import AgentSelectStore
from django.shortcuts import HttpResponse

def select_store(requst):
    store = AgentSelectStore()
    return HttpResponse(store.to_json())
