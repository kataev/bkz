# -*- coding: utf-8 -*-
import django.forms as forms
from django.forms.models import inlineformset_factory
from whs.bill.models import *
from whs.brick.models import *
from django.core.exceptions import ValidationError

class DateForm(forms.Form):
    date = forms.DateField()


class NumberInput(forms.TextInput):
    input_type = 'number'


class BillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.legend = self.Meta.model._meta.verbose_name
        self.auto_id = 'doc_%s'

    class Meta:
        name = 'Bill'
        model = Bill
        fields = ('date', 'number', 'agent', 'seller', 'reason', 'info')
        widgets = {
            'number': NumberInput(attrs={'autocomplete': 'off', 'min': 1}),
            'reason': forms.Textarea(attrs={'rows': 2}),
            'info': forms.Textarea(attrs={'rows': 2}),
            }

    class Media:
        pass


class SoldForm(forms.ModelForm):
    class Meta:
        name = 'Sold'
        verbose_name = Sold._meta.verbose_name
        verbose_name_plural = Sold._meta.verbose_name_plural
        model = Sold #autocomplete="off"
        fields = ('brick', 'amount', 'poddon', 'tara', 'info', 'price', 'delivery')
        widgets = {'brick': forms.TextInput(attrs={'data-widget': 'brick-select'}),
                   'amount': NumberInput(attrs={'autocomplete': 'off', 'min': 1}),
                   'tara': NumberInput(attrs={'autocomplete': 'off', 'min': 0}),
                   'price': NumberInput(attrs={'autocomplete': 'off', 'min': 1, 'step': 0.01}),
                   'delivery': NumberInput(attrs={'autocomplete': 'off', 'step': 0.01}),
                   'info': forms.Textarea(attrs={'rows': 2}),
        }


class TransferForm(forms.ModelForm):
    class Meta:
        name = 'Transfer'
        model = Transfer
        verbose_name = Transfer._meta.verbose_name
        verbose_name_plural = Transfer._meta.verbose_name_plural
        fields = ('brick_from', 'brick_to', 'amount', 'poddon', 'tara', 'info', 'price', 'delivery')
        widgets = {
            'brick_from': forms.TextInput(attrs={'data-widget': 'brick-select'}),
            'brick_to': forms.TextInput(attrs={'data-widget': 'brick-select'}),
            'amount': NumberInput(attrs={'autocomplete': 'off', 'min': 1}),
            'tara': NumberInput(attrs={'autocomplete': 'off', 'min': 0}),
            'price': NumberInput(attrs={'autocomplete': 'off', 'min': 1, 'step': 0.01}),
            'delivery': NumberInput(attrs={'autocomplete': 'off', 'step': 0.01}),
            'info': forms.Textarea(attrs={'rows': 2}),
        }

SoldFactory = inlineformset_factory(Bill, Sold, extra=0, form=SoldForm, )
TransferFactory = inlineformset_factory(Bill, Transfer, extra=0, form=TransferForm, )


class BillFilter(forms.Form):
    date__lte = forms.DateField(required=False, widget=forms.DateInput(attrs={'placeholder': u'Конец периода'}))
    date__gte = forms.DateField(required=False, widget=forms.DateInput(attrs={'placeholder': u'Начало периода'}))
    agent = forms.ModelChoiceField(queryset=Agent.objects.all(), required=False)
    brick = forms.ModelChoiceField(queryset=Brick.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        """ Изменение пустой ичейки для подсказки. """
        super(BillFilter, self).__init__(*args, **kwargs)
        self.fields['agent'].empty_label = u'Выберите контрагента'
