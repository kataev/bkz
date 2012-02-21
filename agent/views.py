# -*- coding: utf-8 -*-
from exceptions import ValueError
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render
from agent.models import Agent

def agents(request):
    Agents = Agent.objects.all()
    paginator = Paginator(Agents, 20) # Show 25 contacts per page

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        agents = paginator.page(page)
    except (EmptyPage, InvalidPage):
        agents = paginator.page(paginator.num_pages)
    return render(request,'agents.html',dict(Agents=agents))