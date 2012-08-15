# -*- coding: utf-8 -*-
import floppyforms as forms
from django.forms.models import inlineformset_factory

from bkz.lab.models import *

class ClayForm(forms.ModelForm):
    class Meta:
        model = Clay

class StoredClayForm(forms.ModelForm):
    class Meta:
        model = StoredClay

class SandForm(forms.ModelForm):
    class Meta:
        model = Sand

class BarForm(forms.ModelForm):
    class Meta:
        model = Bar

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

class SplitSizeWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        get_widget = lambda name:forms.widgets.Input(attrs={'title':name})
        names = (u'Длина',u'Ширина',u'Толщина')
        self.widgets = map(get_widget,names)
        super(forms.MultiWidget, self).__init__(attrs)

    def decompress(self, value):
        if value:
            return map(int,value.split('x'))
        return [None, None, None]

class SplitSizeField(forms.MultiValueField):
    widget = SplitSizeWidget
    hidden_widget = SplitSizeWidget
    def compress(self, data_list):
        return '%dx%dx%d' % data_list

class PressureForm(forms.ModelForm):
#    size = SplitSizeField(label=u'Размеры',widget=SplitSizeWidget(attrs={'autocomplete':'off','class':'input-micro','min':0}))
    class Meta:
        model = Pressure



class FlexionForm(forms.ModelForm):
#    size = SplitSizeField()
    class Meta:
        model = Flexion

class PartForm(forms.ModelForm):
    class Meta:
        model = Part


PartFactory = inlineformset_factory(Batch, Part, PartForm, extra=0)
PressureFactory = inlineformset_factory(Batch, Pressure, PressureForm, extra=6)
FlexionFactory = inlineformset_factory(Batch, Flexion, FlexionForm, extra=6)