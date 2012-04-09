# -*- coding: utf-8 -*-
import datetime
from dateutil.relativedelta import relativedelta

import django.forms as forms
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError

from whs.sale.models import *


class DateForm(forms.Form):
    date = forms.DateField()

    @property
    def value(self):
        if self.is_valid():
            return self.cleaned_data['date']
        else:
            return datetime.date.today()

    def prev(self):
        return self.value - datetime.timedelta(1)
    def next(self):
        return self.value + datetime.timedelta(1)

    def prev_month(self):
        return self.value - relativedelta(months=1)
    def next_month(self):
        return self.value + relativedelta(months=1)


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


class SoldForm(forms.ModelForm):
    class Meta:
        name = 'Sold'
        verbose_name = Sold._meta.verbose_name
        verbose_name_plural = Sold._meta.verbose_name_plural
        model = Sold
        widgets = {'brick': forms.TextInput(attrs={'data-widget': 'brick-select'}),
                   'tara': NumberInput(attrs={'autocomplete': 'off', 'min': 1}),
                   'amount': NumberInput(attrs={'autocomplete': 'off', 'min': 1}),
                   'price': NumberInput(attrs={'autocomplete': 'off', 'min': 1, 'step': 0.01}),
                   'delivery': NumberInput(attrs={'autocomplete': 'off', 'step': 0.01}),
                   'info': forms.Textarea(attrs={'rows': 2}),
        }

    def clean(self):
        data = self.cleaned_data
        brick, amount = data['brick'],data['amount']
        print brick.total
        if brick.total < amount:
            raise ValidationError(u'На складе нету столько кирпича')
        return data


class TransferForm(forms.ModelForm):
    class Meta:
        name = 'Transfer'
        model = Transfer
        verbose_name = Transfer._meta.verbose_name
        verbose_name_plural = Transfer._meta.verbose_name_plural
        widgets = {
            'brick_from': forms.TextInput(attrs={'data-widget': 'brick-select'}),
            'brick_to': forms.TextInput(attrs={'data-widget': 'brick-select'}),
            'tara': NumberInput(attrs={'autocomplete': 'off', 'min': 1}),
            'amount': NumberInput(attrs={'autocomplete': 'off', 'min': 1}),
            'price': NumberInput(attrs={'autocomplete': 'off', 'min': 1, 'step': 0.01}),
            'delivery': NumberInput(attrs={'autocomplete': 'off', 'step': 0.01}),
            'info': forms.Textarea(attrs={'rows': 2}),
        }

    def clean(self):
        data = self.cleaned_data
        brick_from, brick_to, amount = data['brick_from'],data['brick_to'],data['amount']
        if brick_from.mark < brick_to.mark:
            raise ValidationError(u'Нельзя делать перевод из меньшей марки в большую')
        if brick_from.weight != brick_to.weight:
            raise ValidationError(u'Нельзя в переводе менять размер кирпича')
        if brick_from.total < amount:
            raise ValidationError(u'На складе нету столько кирпича для перевода')
        return data

class PalletForm(forms.ModelForm):
    class Meta:
        name = 'Pallet'
        model = Pallet
        verbose_name = Pallet._meta.verbose_name
        verbose_name_plural = Pallet._meta.verbose_name_plural
        widgets = {
            'amount': NumberInput(attrs={'autocomplete': 'off', 'min': 1}),
            'info': forms.Textarea(attrs={'rows': 2}),
            }



SoldFactory = inlineformset_factory(Bill, Sold, extra=0, form=SoldForm)
TransferFactory = inlineformset_factory(Bill, Transfer, extra=0, form=TransferForm, )
PalletFactory = inlineformset_factory(Bill, Pallet, extra=0, form=PalletForm, )

class SoldFactory(SoldFactory):
    def clean(self):
        if any(self.errors):
            return
        bricks = {}
        amounts = {}
        for i in range(0, self.total_form_count()):
            form = self.forms[i]
            brick, amount = form.cleaned_data['brick'],form.cleaned_data['amount']
            bricks[brick.pk] = brick
            amounts[brick.pk] = amounts.get(brick.pk,0) + amount

        for pk in bricks:
            b = bricks[pk]
            if b.total < amounts[pk]:
                raise ValidationError(u'Не хватает кирпича для накладной, проверьте отгрузки по кирпичу %s' % b.label)

class TransferFactory(TransferFactory):
    def clean(self):
        if any(self.errors):
            return
        bricks = {}
        amounts = {}
        for form in self.forms:
            brick, amount = form.cleaned_data['brick_from'],form.cleaned_data['amount']
            bricks[brick.pk] = brick
            amounts[brick.pk] = amounts.get(brick.pk,0) + amount

        for pk in bricks:
            b = bricks[pk]
            if b.total < amounts[pk]:
                raise ValidationError(u'Не хватает кирпича для накладной, проверьте переводы по кирпичу %s' % b.label)

class YearMonthFilter(forms.Form):
    date__year = forms.IntegerField(required=True)
    date__month = forms.IntegerField(required=False)

class BillFilter(forms.Form):
    date__year = forms.IntegerField(required=False)
    date__month = forms.IntegerField(required=False)
    agent = forms.ModelChoiceField(queryset=Agent.objects.all(), required=False)
    brick = forms.ModelChoiceField(queryset=Brick.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        """ Изменение пустой ичейки для подсказки. """
        super(BillFilter, self).__init__(*args, **kwargs)
        self.fields['agent'].empty_label = u'Выберите контрагента'

    class Meta:
        dates = Bill.objects.dates('date','month')


class AgentForm(forms.ModelForm):
    class Meta:
        message = 'Внимательно заполняйте значения имя и полное имя.'
        model=Agent
        widgets = {
            'name': forms.Textarea(attrs=dict(rows=2)),
            'bank': forms.Textarea(attrs=dict(rows=2)),
            'address': forms.Textarea(attrs=dict(rows=2)),
            }

