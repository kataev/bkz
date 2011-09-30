# -*- coding: utf-8 -*-
import dojango.forms as forms
from whs.agent.models import Agent

class AgentForm(forms.ModelForm):
    class Meta:
        model=Agent
        widgets = {
            'bank': forms.Textarea(attrs={}),
            'address': forms.Textarea(attrs={}),
        }
    class Media:
        js = ('js/form.js',)
        css = {'all':('css/form.css',),}

