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

class FlexionInput(forms.TextInput):
    def __init__(self, attrs=None):
        super(FlexionInput, self).__init__(attrs=attrs)
        self.attrs['autocomplete'] = 'off'

class PressureInput(forms.TextInput):
    def __init__(self, attrs=None):
        super(PressureInput, self).__init__(attrs=attrs)
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
            Fieldset(u'Партия','number','date','cavitation','width','color','flexion','pressure','mark','weight','density',css_class='less span5'),
#            Fieldset(u'Характеристики','heatconduction','seonr','frost_resistance','water_absorption',css_class='span7'),
        )

info_list = ['5.3.2 Известняковые включения < 1см','5.3.4 Размеры, дефекты','5.3.3 Высолы','5.2.6 Половняк более 5%','5.2.5 Черная сердцевина, пятна']


class PartForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Part
        exclude = ('amount','tto','brick')
        widgets = {
            'info':forms.Textarea(attrs={'rows':1,"placeholder":'Примечание'}),
            'limestone':forms.TextInput(attrs={"placeholder":'№ ТТО','autocomplete':'off'}),
        }

PartFactory = inlineformset_factory(Batch, Part, PartForm, extra=2,max_num=3)

class RowForm(forms.ModelForm):
    class Meta:
        model = RowPart
        widgets = {
            'tto':forms.TextInput(attrs={'placeholder':'Номера тто','autocomplete':'off'}),
            'dnumber':forms.TextInput(attrs={'title':'Браковочное число','placeholder':'Брак.число'}),
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
        widgets = {
            'tto':forms.TextInput(attrs={'autocomplete':'off'}),
            'row':forms.TextInput(attrs={'autocomplete':'off'}),
            'size':forms.TextInput(attrs={'autocomplete':'off'}),
            'area':forms.TextInput(attrs={'readonly':'readonly','tabindex':-1}),
            'value':forms.TextInput(attrs={'readonly':'readonly','tabindex':-1}),
            }

class FlexionForm(forms.ModelForm):
    class Meta:
        exclude = ('timestamp',)
        model = Flexion
        widgets = {
            'tto':forms.TextInput(attrs={'autocomplete':'off'}),
            'row':forms.TextInput(attrs={'autocomplete':'off'}),
            'size':forms.TextInput(attrs={'autocomplete':'off'}),
            'area':forms.TextInput(attrs={'readonly':'readonly','tabindex':-1}),
            'value':forms.TextInput(attrs={'readonly':'readonly','tabindex':-1}),
            }

PressureFactory = inlineformset_factory(Batch, Pressure, PressureForm, extra=6, max_num=6, can_delete=False)
FlexionFactory  = inlineformset_factory(Batch, Flexion,  FlexionForm,  extra=6, max_num=6, can_delete=False)

marks = [300, 250, 200, 175, 150, 125, 100]
def get_pressure_value(self):
    if len(self.queryset) == 6:
        val = [ x.value for x in self.queryset]
        avg = round(sum(val)/6,2)
        avg_list = [30, 25, 20, 17.5, 15, 12.5, 10]
        min_list = [25, 20, 17.5, 15, 12.5, 10, 7.5]
        mark = max([mark for a,m,mark in zip(avg_list,min_list,marks) if min(val)>m and avg>a] or [0,])
        return {'avgn':avg,'min':avg*0.5,'max':avg*1.5,'avg':avg,'mark':mark}
PressureFactory.get_value = property(get_pressure_value)

def get_flexion_value(self):
    if len(self.queryset) == 6:
        val = [ x.value for x in self.queryset]
        avg = round(sum(val)/6,2)
        valn = filter(lambda x: avg*0.5 < x < avg*1.5, val)
        avgn = round(sum(valn)/len(valn),2)
        if not self.instance.width == 1.4:
             avg_list = [3.4, 2.9, 2.5, 2.3, 2.1, 1.9, 1.6]
             min_list = [1.7, 1.5, 1.3, 1.1, 1.0, 0.9, 0.8]
        else:
             avg_list = [2.9, 2.5, 2.3, 2.1, 1.8, 1.6, 1.4]
             min_list = [1.5, 1.3, 1.0, 1.0, 0.9, 0.8, 0.7]
        mark = max([mark for a,m,mark in zip(avg_list,min_list,marks) if min(val)>m and avg>a] or [0,])
        return {'avgn':avgn,'min':avg*0.5,'max':avg*1.5,'avg':avg,'mark':mark}
FlexionFactory.get_value = property(get_flexion_value)


class BatchTestsForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        model = Batch
        layout = (
            Fieldset(u'Прочее','pf','pct','chamfer',css_class='less span4 form-horizontal'),
            Fieldset(u'Характеристики','heatconduction','seonr','frost_resistance','water_absorption',css_class='span5 form-horizontal'),
        )
