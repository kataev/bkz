# -*- coding: utf-8 -*-
import dojango.forms as forms

from whs.agents.models import agent

class agentForm(ModelForm):
    class Meta:
        model=agent
        widgets = {
            'bank': Textarea(attrs={}),
            'address': Textarea(attrs={}),
        }

class agent_filter_form(ModelForm):
    class Meta:
        model=agent
        field = ['name','form','type','address','inn']