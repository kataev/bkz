# -*- coding: utf-8 -*-
from django import forms

from whs.lab.models import *
from whs.sale.forms import NumberInput


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
        models = Raw

class HalfForm(forms.ModelForm):
    class Meta:
        models = Half

class WaterAbsorptionForm(forms.ModelForm):
    class Meta:
        models = WaterAbsorption

class EfflorescenceForm(forms.ModelForm):
    class Meta:
        model = Efflorescence

class FrostResistanceForm(forms.ModelForm):
    class Meta:
        model = FrostResistance


class DensityForm(forms.ModelForm):
    class Meta:
        model = Density

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch

class PressureForm(forms.ModelForm):
    class Meta:
        model = Pressure

class FlexionForm(forms.ModelForm):
    class Meta:
        model = Flexion