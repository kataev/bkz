# -*- coding: utf-8 -*-
import django.forms as forms
from django.forms.models import inlineformset_factory
from bkz.bootstrap.forms import BootstrapMixin,Fieldset

from bkz.lab.models import *
from bkz.whs.forms import BatchInput,DateInput,NumberInput

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


class BrickChechboxInput(forms.CheckboxInput):
    pass

class BrickInput(forms.Select):
    pass


class BatchDateInput(DateInput):
    pass

class WeightInput(NumberInput):
    def __init__(self, attrs=None):
        super(WeightInput, self).__init__(attrs=attrs)
        self.attrs['step'] = 0.01
        self.attrs['min'] = 0
        self.attrs['autocomplete'] = 'off'

class DensityInput(NumberInput):
    def __init__(self, attrs=None):
        super(DensityInput, self).__init__(attrs=attrs)
        self.attrs['step'] = 0.1
        self.attrs['min'] = 1
        self.attrs['autocomplete'] = 'off'

class FlexionInput(NumberInput):
    def __init__(self, attrs=None):
        super(FlexionInput, self).__init__(attrs=attrs)
        self.attrs['step'] = 0.01
        self.attrs['min'] = 0
        self.attrs['autocomplete'] = 'off'

class PressureInput(NumberInput):
    def __init__(self, attrs=None):
        super(PressureInput, self).__init__(attrs=attrs)
        self.attrs['step'] = 0.01
        self.attrs['min'] = 0
        self.attrs['autocomplete'] = 'off'

class BatchForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        model = Batch
        widgets = {
            'number':BatchInput(),
            'date':BatchDateInput(),
            'cavitation':BrickChechboxInput(attrs={'title':'Пустотелый?'}),
            'width':BrickInput(),
            'color':BrickInput(),
            'weight':WeightInput(),
            'density':DensityInput(),
            'flexion':FlexionInput(),
            'pressure':PressureInput(),

        }
        layout = (
            Fieldset(u'Партия','number','date','cavitation','width','color','weight','density','mark','flexion','pressure','half',css_class='less span5'),
#            Fieldset(u'Характеристики','heatconduction','seonr','frost_resistance','water_absorption',css_class='span7'),
        )

info_list = ['5.3.2 Известняковые включения < 1см','5.3.4 Размеры, дефекты','5.3.3 Высолы','5.2.6 Половняк более 5%','5.2.5 Черная сердцевина, пятна']


class PartForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Part
        exclude = ('amount','tto','brick')
        widgets = {
            'defect':forms.Select(attrs={'class':'span2'}),
            'dnumber':forms.TextInput(attrs={'class':'span1'}),
            'info':forms.Textarea(attrs={'rows':1,"placeholder":'Примечание'}),
        }

PartFactory = inlineformset_factory(Batch, Part, PartForm, extra=2,max_num=3)

class RowForm(forms.ModelForm):
    class Meta:
        model = RowPart
        widgets = {
            'tto':forms.TextInput(attrs={'placeholder':'Номера тто','autocomplete':'off'}),
            'amount':NumberInput(),
            'dnumber':NumberInput(attrs={'title':'Браковочное число','placeholder':'Брак.число'}),
            'brocken':NumberInput(),
            'test':NumberInput(),
            }


RowFactory = inlineformset_factory(Part, RowPart, RowForm,extra=1,max_num=1)

class SplitSizeWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        get_widget = lambda name:forms.widgets.Input(attrs={'title':name})
        names = (u'Длина',u'Ширина',u'Толщина')
        self.widgets = map(get_widget,names)
        super(SplitSizeWidget, self).__init__(attrs)

    def decompress(self, value):
        if value:
            return map(int,value.split('x'))
        return [None, None, None]

class SplitSizeField(forms.MultiValueField):
    widget = SplitSizeWidget
    def compress(self, data_list):
        return '%dx%dx%d' % data_list

class PressureForm(forms.ModelForm):
    class Meta:
        exclude = ('timestamp',)
        model = Pressure

class FlexionForm(forms.ModelForm):
    class Meta:
        exclude = ('timestamp',)
        model = Flexion

PressureFactory = inlineformset_factory(Batch, Pressure, PressureForm, extra=6,max_num=6)
FlexionFactory = inlineformset_factory(Batch, Flexion, FlexionForm, extra=6,max_num=6)