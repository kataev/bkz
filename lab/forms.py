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
    pass

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
        exclude = ('amount','tto')
        widgets = {
            'defect':forms.Select(attrs={'class':'span2'}),
            'dnumber':forms.TextInput(attrs={'class':'span1'}),
            'info':forms.Textarea(attrs={'rows':1,"placeholder":'Примечание'}),
        }

PartFactory = inlineformset_factory(Batch, Part, PartForm, extra=1)

class RowForm(forms.ModelForm):
    class Meta:
        model = RowPart
        widgets = {
            'tto':forms.TextInput(attrs={'placeholder':'Номера тто'}),
            'amount':NumberInput(),
            'dnumber':NumberInput(attrs={'title':'Браковочное число','placeholder':'Брак.число'}),
            'brocken':NumberInput(),
            'test':NumberInput(),
            }


RowFactory = inlineformset_factory(Part, RowPart, RowForm,extra=0)

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
#    size = SplitSizeField(label=u'Размеры',widget=SplitSizeWidget(attrs={'autocomplete':'off','class':'input-micro','min':0}))
    class Meta:
        model = Pressure

class FlexionForm(forms.ModelForm):
#    size = SplitSizeField()
    class Meta:
        model = Flexion

PressureFactory = inlineformset_factory(Batch, Pressure, PressureForm, extra=0)
FlexionFactory = inlineformset_factory(Batch, Flexion, FlexionForm, extra=0)



