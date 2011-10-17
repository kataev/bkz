# -*- coding: utf-8 -*-
__author__ = 'bteam'
from dojango.data.modelstore import *
from whs.agent.models import Agent

class AgentSelectStore(Store):
    label = StoreField('__unicode__')

    class Meta(object):
        objects  = Agent.objects.all()

