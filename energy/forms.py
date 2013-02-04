# -*- coding: utf-8 -*-
__author__ = 'bteam'
import django.forms as forms
from bkz.energy.models import Energy,Teplo

from django.forms.models import modelformset_factory
from bkz.whs.forms import NumberInput,FloatInput,DateInput

class EnergyForm(forms.ModelForm):
    class Meta:
        name = 'Energy'
        model = Energy
        widgets = {
            'date':DateInput(),
            'elec4':FloatInput(),
            'elec16':FloatInput(),
            'iwater':FloatInput(),
            'uwater':FloatInput,
            'gaz':NumberInput(),
            }

EnergyFactory = modelformset_factory(Energy,form=EnergyForm,extra=1)

class TeploForm(forms.ModelForm):
    class Meta:
        name = 'Teplo'
        model = Teplo
        widgets = {
            'date':DateInput(),
            'henergy':FloatInput(),
            'hot_water':FloatInput(),
            'rpr':FloatInput(),
            'robr':FloatInput(),
            'tpr':FloatInput(),
            'tobr':FloatInput(),
            }

TeploFactory = modelformset_factory(Teplo,form=TeploForm,extra=1)