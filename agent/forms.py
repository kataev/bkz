# -*- coding: utf-8 -*-
import dojango.forms as forms

from whs.agent.models import Agent

class AgentForm(ModelForm):
    class Meta:
        model=Agent
        widgets = {
            'bank': Textarea(attrs={}),
            'address': Textarea(attrs={}),
        }

class AgentFilterForm(ModelForm):
    class Meta:
        model=Agent
        field = ['name','form','type','address','inn']