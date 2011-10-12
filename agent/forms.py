# -*- coding: utf-8 -*-
import dojango.forms as forms
from whs.agent.models import Agent

class AgentForm(forms.ModelForm):
    class Meta:
        model=Agent
        widgets = {
            'name': forms.Textarea(),
            'bank': forms.Textarea(),
            'address': forms.Textarea(),
        }
    class Media:
        js = ('js/form.js',)
        css = {'all':('css/form.css',),}

