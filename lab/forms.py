# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory

from bkz.lab.models import *
from bkz.whs.forms import NumberInput


class ClayForm(forms.ModelForm):
    class Meta:
        model = Clay
        widgets = {
            'humidity': forms.TextInput(attrs={'autocomplete': 'off', 'class':'SlashSeparatedFloatField'}),
            'sand': NumberInput(attrs={'autocomplete': 'off', 'step':0.01, 'min':0, 'class':'span1'}),
            'inclusion': NumberInput(attrs={'autocomplete': 'off', 'step':0.01,'min':0, 'class':'span1'}),
            'dust': NumberInput(attrs={'autocomplete': 'off', 'step':0.01, 'min':0, 'class':'span1'}),
            'info': forms.Textarea(attrs={'rows': 2}),
        }


class StoredClayForm(forms.ModelForm):
    class Meta:
        model = StoredClay
        widgets = {
#            'position': forms.TextInput(attrs={'autocomplete': 'off', 'class':'span1'}),
            'humidity': NumberInput(attrs={'autocomplete': 'off', 'step':0.01, 'min':0, 'class':'span1'}),
            'info': forms.Textarea(attrs={'rows': 2}),
            }

class SandForm(forms.ModelForm):
    class Meta:
        model = Sand
        widgets = {
            'humidity': forms.TextInput(attrs={'autocomplete': 'off', 'class':'SlashSeparatedFloatField'}),
            'particle_size': NumberInput(attrs={'autocomplete': 'off', 'step':0.01, 'min':0, 'class':'span1'}),
            'module_size': NumberInput(attrs={'autocomplete': 'off', 'step':0.01,'min':0, 'class':'span1'}),
            'dirt': forms.Textarea(attrs={'rows': 2}),
            'info': forms.Textarea(attrs={'rows': 2}),
            }

class BarForm(forms.ModelForm):
    class Meta:
        model = Bar
        widgets = {
            'humidity': forms.TextInput(attrs={'autocomplete': 'off', 'class':'span1'}),
            'tts': forms.TextInput(attrs={'autocomplete': 'off', 'class':'span1'}),
            'temperature': NumberInput(attrs={'autocomplete': 'off', 'step':0.01,'min':0, 'class':'span1'}),
            'weight': NumberInput(attrs={'autocomplete': 'off', 'step':1,'min':0, 'class':'span1'}),
            'dirt': forms.Textarea(attrs={'rows': 2}),
            'info': forms.Textarea(attrs={'rows': 2}),
            }

class RawForm(forms.ModelForm):
    class Meta:
        model = Raw

class HalfForm(forms.ModelForm):
    class Meta:
        model = Half

class WaterAbsorptionForm(forms.ModelForm):
    class Meta:
        model = WaterAbsorption

class EfflorescenceForm(forms.ModelForm):
    class Meta:
        model = Efflorescence

class FrostResistanceForm(forms.ModelForm):
    class Meta:
        model = FrostResistance

class SEONRForm(forms.ModelForm):
    class Meta:
        model = SEONR

class HeatConductionForm(forms.ModelForm):
    class Meta:
        model = HeatConduction

class DensityForm(forms.ModelForm):
    class Meta:
        model = Density

class DateHTML5Input(forms.DateInput):
    input_type = 'date'

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        widgets = {
            'number':NumberInput(attrs={'autocomplete':'off','class':'input-mini','min':1}),
            'date':DateHTML5Input(attrs={'autocomplete':'off','class':'input-small'})
        }

class PartForm(forms.ModelForm):
    class Meta:
        model = Part


class PressureForm(forms.ModelForm):
    class Meta:
        model = Pressure

class FlexionForm(forms.ModelForm):
    class Meta:
        model = Flexion
        widgets = {
            'number': forms.TextInput(attrs={'autocomplete': 'off', 'class':'span1'}),
            'water_absorption': forms.Select(attrs={'class':'span3'}),

#            'tts': forms.TextInput(attrs={'autocomplete': 'off', 'class':'span1'}),
#            'temperature': NumberInput(attrs={'autocomplete': 'off', 'step':0.01,'min':0, 'class':'span1'}),
#            'weight': NumberInput(attrs={'autocomplete': 'off', 'step':1,'min':0, 'class':'span1'}),
#            'dirt': forms.Textarea(attrs={'rows': 2}),
            'inclusion': forms.Textarea(attrs={'rows': 2}),
            'info': forms.Textarea(attrs={'rows': 2}),
            }


PartFactory = inlineformset_factory(Batch, Part, PartForm, extra=0)
PressureFactory = inlineformset_factory(Batch, Pressure, PressureForm, extra=0)
FlexionFactory = inlineformset_factory(Batch, Flexion, FlexionForm, extra=0)