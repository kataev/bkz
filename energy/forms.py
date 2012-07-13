# -*- coding: utf-8 -*-
__author__ = 'bteam'
import django.forms as forms
from bkz.energy.models import *


class EnergyForm(forms.ModelForm):
    class Meta:
        name = 'Energy'
        model = Energy
        buttons = {'right':[(u'energy:Energy-delete','btn btn-danger',u'Удалить',),]}
        widgets = {
            'date':forms.TextInput(attrs={'class':'input-small'}),
            'elec4':forms.TextInput(attrs={'class':'input-small'}),
            'elec16':forms.TextInput(attrs={'class':'input-small'}),
            'iwater':forms.TextInput(attrs={'class':'input-small'}),
            'uwater':forms.TextInput(attrs={'class':'input-small'}),
            'gaz':forms.TextInput(attrs={'class':'input-small'}),
            }

class TeploForm(forms.ModelForm):
    class Meta:
        name = 'Teplo'
        model = Teplo
        buttons = {'right':[(u'Energy:Teplo-delete','btn btn-danger',u'Удалить',)]}
        widgets = {
            'date':forms.TextInput(attrs={'class':'input-small'}),
            'henergy':forms.TextInput(attrs={'class':'input-small'}),
            'hot_water':forms.TextInput(attrs={'class':'input-small'}),
            'rpr':forms.TextInput(attrs={'class':'input-small'}),
            'robr':forms.TextInput(attrs={'class':'input-small'}),
            'tpr':forms.TextInput(attrs={'class':'input-small'}),
            'tobr':forms.TextInput(attrs={'class':'input-small'}),
            }