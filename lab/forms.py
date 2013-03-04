# -*- coding: utf-8 -*-
import django.forms as forms
from django.forms.models import inlineformset_factory, modelformset_factory
from bkz.bootstrap.forms import BootstrapMixin

from bkz.whs.models import Width
from bkz.lab.models import *
from bkz.whs.forms import BatchInput,DateInput,NumberInput,FloatInput


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

class PopUpCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    pass



class MatherialForm(BootstrapMixin,forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MatherialForm, self).__init__(*args,**kwargs)
        position = (self.instance.position or self.initial.get('position'))
        if position < 8:
            self.fields['position'].choices = self.fields['position'].choices[:8]
            if 'sand' in self.fields.keys():
                self.fields['sand'].widget = forms.HiddenInput(attrs={})
            if 'dust' in self.fields.keys():
                self.fields['dust'].widget = forms.HiddenInput(attrs={})
                self.fields['particle_size'].widget = forms.HiddenInput(attrs={})
                self.fields['module_size'].widget = forms.HiddenInput(attrs={})
        elif position < 8:
            self.fields['position'].choices = self.fields['position'].choices[position:position+1]
        if position == 8:
            self.fields['module_size'].label = u'Глинистые'
            self.fields['dust'].label = u'Пластичность'
            self.fields['particle_size'].label = u'Пылеватые'
            self.fields['position'].widget = forms.HiddenInput(attrs={})
    class Meta:
        model = Matherial
        widgets = {'datetime':SplitDateTimeHTML5Widget,
                    'humidity':FloatInput(attrs={'autocomplete':'off'}),
                    'sand':FloatInput(attrs={'autocomplete':'off'}),
                    'inclusion':FloatInput(attrs={'autocomplete':'off'}),
                    'dust':FloatInput(attrs={'autocomplete':'off'}),
                    'particle_size':FloatInput(attrs={'autocomplete':'off'}),
                    'module_size':FloatInput(attrs={'autocomplete':'off'}),
        }


QuarryFactory = modelformset_factory(Matherial,form=MatherialForm,extra=3,max_num=3)
QuarryFactory.caption = u'Карьер'
QuarryFactory.css_class = 'span6'
QuarryFactory.width = {}

class ClayForm(MatherialForm):
    class Meta(MatherialForm.Meta):
        fields = ('datetime','position','humidity')


ClayFactory = modelformset_factory(Matherial,form=ClayForm,extra=3,max_num=10)
ClayFactory.caption = u'Склад'
ClayFactory.css_class = 'span4'
ClayFactory.width = {}

class SandForm(MatherialForm):
    def __init__(self, *args, **kwargs):
        super(SandForm, self).__init__(*args,**kwargs)
        self.css_class = 'span2 form-horizontal less Sand'
    class Meta(MatherialForm.Meta):
        exclude = ('position','info')


MatherialFactory = modelformset_factory(Matherial,form=MatherialForm,extra=2,max_num=10)
MatherialFactory.caption = u'Сырьё'
MatherialFactory.css_class = 'span12'
MatherialFactory.width = {}


class BarForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        exclude = ("cutter","info",'cavitation','color','width','forming')
        model = Bar
        widgets = {'datetime':SplitDateTimeHTML5Widget,
                'tts':NumberInput,
                'weight':NumberInput,
                'temperature':NumberInput,
                'humidity':FloatInput,
                'sand':FloatInput,
                'humidity_transporter':FloatInput,
        }
BarFactory = modelformset_factory(Bar,form=BarForm,extra=2,max_num=4)
BarFactory.caption = u'Формовка'
BarFactory.css_class = 'span12'
BarFactory.width = {}


class RawForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        exclude = (u'info','cavitation','color','width','forming')
        model = Raw
        widgets = {'datetime':SplitDateTimeHTML5Widget,
                    'tts':NumberInput,
                    'weight':NumberInput,
                    'temperature':NumberInput,
                    'humidity':FloatInput,
        }


RawFactory = modelformset_factory(Raw,form=RawForm,extra=1)
RawFactory.caption = u'Накопитель'
RawFactory.css_class = 'span6'
RawFactory.width = {}


class HalfForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        exclude = (u'info','cavitation','color','width','forming'   )
        model = Half
        widgets = { 'datetime':SplitDateTimeHTML5Widget,
                    'weight':NumberInput,
                    'temperature':NumberInput,
                    'humidity':FloatInput,
                    'shrink':FloatInput,
                    'position':NumberInput(attrs={'max':25,'min':1,'step':1}),
                    'path':NumberInput(attrs={'max':7,'min':4,'step':1}),
                    'cause':PopUpCheckboxSelectMultiple(attrs={'class':'checkbox'}),
        }

HalfFactory = modelformset_factory(Half,form=HalfForm,extra=4,max_num=8)
HalfFactory.caption = u'Полуфабрикат'
HalfFactory.css_class = 'span6'
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

class CauseForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        model = Cause

class BatchForm(BootstrapMixin,forms.ModelForm):
    class Meta:
        model = Batch
        fields = ('number', 'date', 'cavitation', 'width','color', 'flexion', 'pressure', 'mark', 'weight', 'cad', 'info')
        exclude = ('ctype','view')
        widgets = {
            'number':BatchInput(),
            'date':BatchDateInput(),
            'weight':NumberInput(),
            'flexion':FlexionInput(),
            'pressure':PressureInput(),
            'info':forms.Textarea(attrs={'rows':3,"placeholder":'Примечание'}),
        }

info_list = ['5.3.2 Известняковые включения < 1см','5.3.4 Размеры, дефекты','5.3.3 Высолы','5.2.6 Половняк более 5%','5.2.5 Черная сердцевина, пятна']

class PartForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Part
        exclude = ('amount','tto','brick')
        widgets = {
            # 'info':forms.Textarea(attrs={'rows':1,"placeholder":'Примечание'}),
            'half':FloatInput,
            'dnumber':FloatInput,
            'limestone':forms.TextInput(attrs={"placeholder":'№ ТТО с известняком',
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
        return {'avgn':avg,'min':round(avg*0.5,2),'max':round(avg*1.5,2),'avg':avg,'mark':mark}
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
        return {'avgn':avgn,'min':round(avg*0.5,2),'max':round(avg*1.5,2),'avg':avg,'mark':mark}
FlexionFactory.get_value = property(get_flexion_value)
FlexionFactory.caption = u'Испытания на изгиб'

class BatchTestsForm(BootstrapMixin,forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(BatchTestsForm, self).__init__(*args,**kwargs)
        choices = []
        for k,v in self['cad'].field.choices:
            if k:
                v = '%s %s' % (k,v)
            choices.append((k,v))
        self['cad'].field.choices = choices

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
    ('Matherial',u'Сырьё'),
    ('Bar',u'Формовка'),
    ('Raw',u'Сырец'),
    ('Half',u'Полуфабрикат'),
    )

position_c = (
    (u'Сырьё', (
        (0,u'Склад глины'),
        (6,u'Конвейер'),
        (7,u'Белая глина'),
        (8,u'Карьер'),
        (9,u'Песок'), ) ),
    (u'Полуфабрикат', (
        (16,u'16 позиция'),
        (25,u'25 позиция')
        ) ),
    )

path_c = (
    (5,u'5 путь'),
    (7,u'7 путь')
    )

class ModelSelect(forms.Form):
    model = forms.ChoiceField(choices=model_c)
    position = forms.ChoiceField(choices=position_c,required=False)
    path = forms.ChoiceField(choices=path_c,required=False)
