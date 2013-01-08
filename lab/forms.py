# -*- coding: utf-8 -*-
import django.forms as forms
from django.forms.models import inlineformset_factory, modelformset_factory
from bkz.bootstrap.forms import BootstrapMixin,Fieldset

from bkz.whs.models import Width
from bkz.lab.models import *
from bkz.whs.forms import BatchInput,DateInput,NumberInput


class SplitDateTimeHTML5Widget(forms.SplitDateTimeWidget):
    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (forms.DateInput(attrs=attrs, format=date_format),
                   forms.TimeInput(attrs=attrs, format='%H:%M'))
        widgets[0].input_type = 'date'
        widgets[1].input_type = 'time'
        super(forms.SplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self,value):
        if value:
            return [value.date(),value.time().replace(second=0,microsecond=0)]
        return [None, None]

class DateHTML5Input(forms.DateInput):
    input_type = 'date'

class FloatInput(NumberInput):
    def __init__(self, attrs=None):
        super(NumberInput, self).__init__(attrs=attrs)
        self.attrs['autocomplete'] = 'off'
        self.attrs['step'] = 0.01

class BrickChechboxInput(forms.CheckboxInput):
    pass

class BrickInput(forms.Select):
    pass


class BatchDateInput(DateInput):
    pass

class FlexionInput(FloatInput):
    pass

class PressureInput(FloatInput):
    pass

class ClayForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        model = Clay
        exclude = (u'info',)
        widgets = {'datetime':SplitDateTimeHTML5Widget,
                    'humidity':forms.TextInput(attrs={'class':"SlashSeparatedFloatField",'autocomplete':'off'}),
                    'sand':FloatInput,
                    'inclusion':FloatInput,
                    'dust':FloatInput,
        }

ClayFactory = modelformset_factory(Clay,form=ClayForm,extra=1)
ClayFactory.caption = u'Глина из карьера'
ClayFactory.css_class = 'span7'
ClayFactory.label_style = {}

class StoredClayForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        exclude = (u'info',)
        model = StoredClay
        widgets = {'datetime':SplitDateTimeHTML5Widget,
                    'humidity':FloatInput(attrs={'autocomplete':'off'}),
        }

StoredClayFactory = modelformset_factory(StoredClay,form=StoredClayForm,extra=5,max_num=6)
StoredClayFactory.caption = u'Глина по позициям'
StoredClayFactory.css_class = 'span5'
StoredClayFactory.width = {}

class SandForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        exclude = (u'info',)
        model = Sand
        widgets = {
                'datetime':SplitDateTimeHTML5Widget,
                'humidity':FloatInput(attrs={'autocomplete':'off'}),
                'particle_size':FloatInput(attrs={'autocomplete':'off'}),
                'module_size':FloatInput(attrs={'autocomplete':'off'}),
                }

SandFactory = modelformset_factory(Sand,form=SandForm,extra=1)
SandFactory.caption = u'Песок'
SandFactory.css_class = 'span6'
SandFactory.width = {}

class BarForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        exclude = ("poke_left","poke_right","stratcher_left","stratcher_right","cutter","info",'cavitation','color','width')
        model = Bar
        widgets = {'datetime':SplitDateTimeHTML5Widget,
                'tts':NumberInput,
                'weight':NumberInput,
                'temperature':FloatInput,
                'humidity':FloatInput,
                'sand':FloatInput,
                'humidity_transporter':FloatInput,
        }
BarFactory = modelformset_factory(Bar,form=BarForm,extra=1)
BarFactory.caption = u'Формовка'
BarFactory.css_class = 'span10'
BarFactory.width = {}


class RawForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        exclude = (u'info','cavitation','color','width')
        model = Raw
        widgets = {'datetime':SplitDateTimeHTML5Widget,
                    'tts':NumberInput,
                    'weight':NumberInput,
                    'temperature':FloatInput,
                    'humidity':FloatInput,
        }


RawFactory = modelformset_factory(Raw,form=RawForm,extra=1)
RawFactory.caption = u'Сырец'
RawFactory.css_class = 'span9'
RawFactory.width = {}


class HalfForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        exclude = (u'info','cavitation','color','width')
        model = Half
        widgets = { 'datetime':SplitDateTimeHTML5Widget,
                    'weight':NumberInput,
                    'temperature':FloatInput,
                    'humidity':FloatInput,
                    'shrink':FloatInput,
        }

HalfFactory = modelformset_factory(Half,form=HalfForm,extra=4,max_num=4)
HalfFactory.caption = u'Полуфабрикат'
HalfFactory.css_class = 'span9'
HalfFactory.width = {}

class WaterAbsorptionForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        model = WaterAbsorption

class EfflorescenceForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        model = Efflorescence

class FrostResistanceForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        model = FrostResistance

class SEONRForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        model = SEONR

class HeatConductionForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        model = HeatConduction

class BatchForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        model = Batch
        widgets = {
            'number':BatchInput(),
            'date':BatchDateInput(),
            'weight':FloatInput(),
            'flexion':FlexionInput(),
            'pressure':PressureInput(),
            'info':forms.Textarea(attrs={'rows':3,"placeholder":'Примечание'}),
        }
        layout = (
            Fieldset(u'Партия', 'number', 'date', 'cavitation', 'width', 'view',
                'color', 'ctype', 'flexion', 'pressure', 'mark', 'weight', 'cad', 'info',
                css_class='less span5'),
        )

info_list = ['5.3.2 Известняковые включения < 1см','5.3.4 Размеры, дефекты','5.3.3 Высолы','5.2.6 Половняк более 5%','5.2.5 Черная сердцевина, пятна']

class PartForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Part
        exclude = ('amount','tto','brick')
        widgets = {
            # 'info':forms.Textarea(attrs={'rows':1,"placeholder":'Примечание'}),
            'half':FloatInput,
            'dnumber':FloatInput,
            'limestone':forms.TextInput(attrs={"placeholder":'№ ТТО с извесняком',
                'title':u'Можно узкаывать через запятую или тире','autocomplete':'off'}),
        }
PartFactory = inlineformset_factory(Batch, Part, PartForm, extra=2,max_num=3)

class RowForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        model = RowPart
        widgets = {
            'tto':forms.TextInput(attrs={'placeholder':'Номера ТТО',
                'title':u'Можно узкаывать через запятую или тире','autocomplete':'off'}),
            'amount':NumberInput,
            'brocken':NumberInput,
            'test':NumberInput,
            'dnumber':forms.TextInput(attrs={'title':'Браковочное число','placeholder':'Брак.число'}),
            }

RowFactory = inlineformset_factory(Part, RowPart, RowForm,extra=1,max_num=1)

class PressureForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        exclude = ('timestamp',)
        model = Test
        widgets = {
            'tto':forms.TextInput(attrs={'autocomplete':'off'}),
            'row':forms.TextInput(attrs={'autocomplete':'off'}),
            'size':forms.TextInput(attrs={'autocomplete':'off'}),
            'area':forms.TextInput(attrs={'readonly':'readonly','tabindex':-1}),
            'value':forms.TextInput(attrs={'readonly':'readonly','tabindex':-1}),
            'type':forms.HiddenInput
            }

class FlexionForm(BootstrapMixin,forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FlexionForm, self).__init__(*args,**kwargs)
        self['area'].label = u'2Bh²'
    class Meta:
        exclude = ('timestamp',)
        model = Test
        widgets = {
            'tto':forms.TextInput(attrs={'autocomplete':'off'}),
            'row':forms.TextInput(attrs={'autocomplete':'off'}),
            'size':forms.TextInput(attrs={'autocomplete':'off'}),
            'area':forms.TextInput(attrs={'readonly':'readonly','tabindex':-1}),
            'value':forms.TextInput(attrs={'readonly':'readonly','tabindex':-1}),
            'type':forms.HiddenInput
            }

PressureFactory = inlineformset_factory(Batch, Test, PressureForm, extra=6, max_num=6, can_delete=False)
FlexionFactory  = inlineformset_factory(Batch, Test,  FlexionForm,  extra=6, max_num=6, can_delete=False)

marks = [300, 250, 200, 175, 150, 125, 100]
def get_pressure_value(self):
    queryset = self.get_queryset()
    if len(queryset) == 6:
        val = [ x.value for x in queryset]
        avg = round(sum(val)/6,2)
        avg_list = [30, 25, 20, 17.5, 15, 12.5, 10]
        min_list = [25, 20, 17.5, 15, 12.5, 10, 7.5]
        mark = max([mark for a,m,mark in zip(avg_list,min_list,marks) if min(val)>m and avg>a] or [0,])
        return {'avgn':avg,'min':avg*0.5,'max':avg*1.5,'avg':avg,'mark':mark}
PressureFactory.get_value = property(get_pressure_value)
PressureFactory.caption = u'Испытания на сжатие'

def get_flexion_value(self):
    queryset = self.get_queryset()
    if len(queryset) == 6:
        val = [ x.value for x in queryset]
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
FlexionFactory.caption = u'Испытания на изгиб'

class BatchTestsForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        model = Batch
        fields = ('heatconduction','seonr','frost_resistance','water_absorption','chamfer',
            'pressure','flexion','weight','density','cad')
        widgets = { 
            'flexion':forms.HiddenInput,
            'pressure':forms.HiddenInput,
            'chamfer':NumberInput,
            }

class BatchFilter(BatchForm):
    width = forms.ModelChoiceField(queryset=Width.objects.all(),required=False)
    def __init__(self,*args,**kwargs):
        super(BatchFilter, self).__init__(*args,**kwargs)
        self.fields['color'].choices = [('', 'Цвет'),] + self.fields['color'].choices
        self.fields['color'].required = False
        self.fields['color'].initial = None
        self.fields['cavitation'].choices = [('', 'Пустоность'),] + self.fields['cavitation'].choices
        self.fields['cavitation'].required = False
        self.fields['cavitation'].initial = None
        

    class Meta:
        fields = ('cavitation','width','color','mark')
        model = Batch

from bkz.whs.forms import BrickSelect
class PartAddForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        fields = ('brick',)
        widgets = {'brick':BrickSelect}
        model = Part

PartAddFormSet = modelformset_factory(Part,form=PartAddForm, extra=0)


model_c = (
    ('Clay',u'Глина из карьера'),
    ('StoredClay',u'Глина по позициям'),
    ('Sand',u'Песок'),
    ('Bar',u'Формовка'),
    ('Raw',u'Сырец'),
    ('Half',u'Полуфабрикат'),
    )

class ModelSelect(forms.Form):
    model = forms.ChoiceField(choices=model_c)