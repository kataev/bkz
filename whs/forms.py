# -*- coding: utf-8 -*-
import datetime
from dateutil.relativedelta import relativedelta
from collections import defaultdict

import floppyforms as forms
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError

from whs.models import *
from whs.validation import validate_transfer

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


class BillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.legend = self.Meta.model._meta.verbose_name
        self.auto_id = 'doc_%s'

    class Meta:
        model = Bill
        verbose_name_accusative = u"Накладную"
        fields = ('date', 'number', 'agent', 'seller', 'reason', 'info')

class SoldForm(forms.ModelForm):
    class Meta:
        model = Sold

    def clean(self):
        data = self.cleaned_data
        brick_from, brick, amount = data['brick_from'],data['brick'],data['amount']
        total = brick.total
        if brick_from:
            validate_transfer(brick_from,brick)
            total = brick_from.total
        if self.instance.pk:
            total +=self.instance.amount
        if total < amount:
            raise ValidationError(u'На складе нету столько кирпича')
        return data


class PalletForm(forms.ModelForm):
    class Meta:
        model = Pallet

SoldFactory = inlineformset_factory(Bill, Sold, SoldForm, extra=2)
PalletFactory = inlineformset_factory(Bill, Pallet, PalletForm, extra=2)

class SoldFactory(SoldFactory):
    def clean(self):
        if any(self.errors):
            return
        bricks, amounts = {},defaultdict(int)
        for form in self.forms:
            brick_from, brick, amount = form.cleaned_data['brick_from'],form.cleaned_data['brick'],form.cleaned_data['amount']
            if brick_from:
                id = brick_from.pk
            else:
                id = brick.pk
            amounts[id] += amount
            if form.instance.pk:
                amounts[id] -= form.instance.amount
        for id in bricks:
            b = bricks[id]
            if b.total < amounts[id]:
                raise ValidationError(u'Не хватает кирпича для накладной, проверьте отгрузки по кирпичу %s' % b.label)

class YearMonthFilter(forms.Form):
    date__year = forms.IntegerField(required=True)
    date__month = forms.IntegerField(required=False)
    class Meta:
        dates = Bill.objects.dates('date','month')[::-1]

records_per_page = (
    (10,'10 записей на странице'),
    ('','20 записей на странице'),
    (50,'50 записей на странице'),
    (100,'100 записей на странице'),
)

class BillFilter(forms.Form):
    page = forms.IntegerField(required=False)
    year = forms.IntegerField(required=False)
    month = forms.IntegerField(required=False)
    agent = forms.ModelChoiceField(queryset=Agent.objects.all(), required=False)
    brick = forms.ModelChoiceField(queryset=Brick.objects.all(), required=False)
    rpp = forms.ChoiceField(choices=records_per_page,initial='',required=False)

    class Meta:
        dates = Bill.objects.dates('date','month').reverse()

bill_group_by = (
    ('seller',u'Продавцу'),
    ('agent',u'Покупателю'),
    ('brick',u'Кирпичу'),
    ('brick_from',u'Кирпичу перевода'),
)


class BillAggregateFilter(BillFilter):
    seller = forms.ModelChoiceField(queryset=Seller.objects.all(), required=False)
    group_by = forms.MultipleChoiceField(choices=bill_group_by)


class AgentForm(forms.ModelForm):
    class Meta:
        model=Agent

agent_choices = (
    (0,'Выбрать'),
    (1,'Создать'),
)

class AgentCreateOrSelectForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.all(), required=False,)

class SellerForm(forms.ModelForm):
    class Meta:
        model=Seller

class AddForm(forms.ModelForm):
    class Meta:
        model = Add

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory

class SortingForm(forms.ModelForm):
    class Meta:
        model = Sorting

class Write_offForm(forms.ModelForm):
    class Meta:
        model = Write_off

Write_offFactory = inlineformset_factory(Inventory, Write_off, extra=0, form=Write_offForm, )

class BrickForm(forms.ModelForm):
    class Meta:
        model=Brick
        exclude = ('total','css','label')

    def clean(self):
        b = self.save(commit=False)
        try:
            b = Brick.objects.exclude(pk=b.pk).get(label=make_label(b))
        except Brick.DoesNotExist:
            return self.cleaned_data
        else:
            raise ValidationError(u'Такой кирпич вроде уже есть с УИД %d!' % b.pk)

class VerificationForm(forms.Form):
    csv = forms.FileField(label=u'Файл в формате csv')
    id = forms.IntegerField(initial=1,label=u'Номер столбца с УИД')
    field = forms.IntegerField(initial=10,label=u'Номер столбца для сверки')