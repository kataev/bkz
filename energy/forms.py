# -*- coding: utf-8 -*-
__author__ = 'bteam'
import django.forms as forms
from whs.energy.models import *


class EnergyForm(forms.ModelForm):
    class Meta:
        name = 'Energy'
        model = Energy

#        widgets = {
#            'number': NumberInput(attrs={'autocomplete': 'off', 'min': 1}),
#            'reason': forms.Textarea(attrs={'rows': 2}),
#            'info': forms.Textarea(attrs={'rows': 2}),
#            }


class TeploForm(forms.ModelForm):
    class Meta:
        name = 'Teplo'
        model = Teplo