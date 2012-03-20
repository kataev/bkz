# -*- coding: utf-8 -*-
import django.forms as forms
from whs.agent.models import Agent

class AgentForm(forms.ModelForm):
    class Meta:
        message = 'Внимательно заполняйте значения имя и полное имя.'
        model=Agent
        widgets = {
            'name': forms.Textarea(attrs=dict(rows=2)),
            'bank': forms.Textarea(attrs=dict(rows=2)),
            'address': forms.Textarea(attrs=dict(rows=2)),
        }

