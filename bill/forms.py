# -*- coding: utf-8 -*-
from brick.forms import BrickSelect,BrickSelectStack
from whs.bill.models import *
from whs.brick.models import Brick

from dojango import forms
from django.forms.util import flatatt
from django.utils.safestring import mark_safe

class FKSelect(forms.SelectMultiple):
#    pass
    dojo_type = 'whs.form.FKSelect'

    def render(self, name, value, attrs=None, choices=()):
        """ Переопределние метода для вывода нужного тега. """
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name,value=value)
        output = [u'<input%s/>' % flatatt(final_attrs)]
        return mark_safe(u'\n'.join(output))


class SoldForm(forms.ModelForm):
    class Meta:
        model = Sold
        exclude = ('post')
        widgets = {
            'doc': forms.HiddenInput(),
            'info': forms.Textarea(attrs={}),
            'brick': BrickSelectStack(),
            'transfer': forms.HiddenInput(),
            'tara': forms.NumberSpinnerInput(
                attrs={'style': 'width:90px;', 'constraints': {'min': 1, 'max': 2000, 'places': 0}}),
            'price': forms.NumberSpinnerInput(attrs={'style': 'width:90px;', 'constraints': {'min': 0, 'max': 200}}),
            'delivery': forms.NumberSpinnerInput(attrs={'style': 'width:90px;', 'constraints': {'min': 0, 'max': 200}})
        }
    class Media:
        js = ('js/form.js','js/form/Sold.js')
        css = {'all': ('css/form.css',), }


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        widgets = {
            'doc': forms.HiddenInput(),
            'info': forms.Textarea(attrs={}),
            'brick': BrickSelectStack(),
            'tara': forms.NumberSpinnerInput(
                attrs={'style': 'width:90px;', 'constraints': {'min': 1, 'max': 2000, 'places': 0}})
        }
    class Media:
        js = ('js/form.js','js/form/Sold.js')
        css = {'all': ('css/form.css',), }


class BillForm(forms.ModelForm):
    sold = forms.ModelMultipleChoiceField(queryset=Sold.objects.all(),widget=FKSelect,required=False)
    transfer = forms.ModelMultipleChoiceField(queryset=Transfer.objects.all(),widget=FKSelect,required=False)

    class Meta:
        model = Bill
        exclude = ('money')
        widgets = {
            'info': forms.Textarea(),
            'agent': forms.FilteringSelect(),
            }
    class Media:
        js = ('js/form.js',)
        css = {'all': ('css/form.css',), }


class Confirm(forms.Form):
    confirm = forms.BooleanField(initial=False)


class Bills(forms.Form):
    date__lte = forms.DateField(required=False, widget=forms.DateInput(attrs={'placeholder': u'Конец периода'}))
    date__gte = forms.DateField(required=False, widget=forms.DateInput(attrs={'placeholder': u'Начало периода'}))
    agent = forms.ModelChoiceField(queryset=Agent.objects.all(), required=False, widget=forms.FilteringSelect())
    brick = forms.ModelChoiceField(queryset=Brick.objects.all(), widget=BrickSelect, required=False)

    def __init__(self, *args, **kwargs):
        """
        Изменение пустой ичейки для подсказки.
        """
        super(Bills, self).__init__(*args, **kwargs)
        self.fields['agent'].empty_label = u'Выберите контрагента'
    class Media:
        js = ('js/bills.js',)
        css = {'all': ('css/bills.css',), }