# -*- coding: utf-8 -*-
from whs.bill.models import *
from whs.brick.models import Brick

from dojango import forms
from django.utils.encoding import force_unicode
from itertools import chain
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.contrib.humanize.templatetags.humanize import intcomma

class BrickSelect(forms.Select):
    dojo_type = 'whs.brickSelect'

    def render(self, name, value, attrs=None, choices=()):
        """
        Переопределние метода для вывода нужного тега.
        """
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select%s>' % flatatt(final_attrs)]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append(u'</select>')
        return mark_safe(u'\n'.join(output))

    def render_option(self, brick, selected_choices, option_value=None, option_label=None):
        """
        Переопределние метода для вывода элемента тега с нужными тегами.
        """
        if brick is None:
            return u''
        else:
            selected_html = ((brick.pk in selected_choices) or (
            str(brick.pk) in selected_choices)) and u' selected="selected"' or ''
            return u'<option dojoType="whs.brick_tr" class="%(class)s" total="%(total)s" value="%(pk)s"%(selected_html)s>%(title)s</option>' % {
                'class': brick.show_css(),
                'total': intcomma(brick.total),
                'pk': brick.pk,
                'selected_html': selected_html,
                'title': brick

            }

    def render_options(self, choices, selected_choices):
        selected_choices = set([v for v in selected_choices])
        output = []
        br = self.choices.queryset
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    try:
                        val = int(option_value)
                        output.append(self.render_option(br.get(pk=val), selected_choices, *option))
                    except ValueError:
                        output.append(self.render_option(None, selected_choices, *option))
                output.append(u'</optgroup>')
            else:
                try:
                    val = br.get(pk=option_value)
                except:
                    val = None
                output.append(self.render_option(val, selected_choices))
        return u'\n'.join(output)

class SoldForm(forms.ModelForm):
    class Meta:
        model = Sold
        exclude = ('post')
        widgets = {
            'doc': forms.HiddenInput(),
            'info': forms.Textarea(attrs={}),
            'brick': BrickSelect(),
            'tara': forms.NumberSpinnerInput(
                attrs={'style': 'width:90px;', 'constraints': {'min': 1, 'max': 2000, 'places': 0}}),
            'price': forms.NumberSpinnerInput(attrs={'style': 'width:90px;', 'constraints': {'min': 0, 'max': 200}}),
            'delivery': forms.NumberSpinnerInput(attrs={'style': 'width:90px;', 'constraints': {'min': 0, 'max': 200}})
        }
    class Media:
        js = ('form.js',)
        css = {'all': ('form.css',), }


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        widgets = {
            'doc': forms.HiddenInput(),
            'info': forms.Textarea(attrs={}),
            'brick': BrickSelect(),
            'sold': forms.HiddenInput(),
            'tara': forms.NumberSpinnerInput(
                attrs={'style': 'width:90px;', 'constraints': {'min': 1, 'max': 2000, 'places': 0}})
        }
    class Media:
        js = ('form.js',)
        css = {'all': ('form.css',), }


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        exclude = ('money')
        widgets = {
            'info': forms.Textarea(attrs={}),
            'agent': forms.FilteringSelect(),
            }
    class Media:
        js = ('form.js','bills.js')
        css = {'all': ('form.css',), }


class Confirm(forms.Form):
    confirm = forms.BooleanField(initial=False)


class Bills(forms.Form):
    date__lte = forms.DateField(required=False, widget=forms.DateInput(attrs={'placeholder': u'Начало периода'}))
    date__gte = forms.DateField(required=False, widget=forms.DateInput(attrs={'placeholder': u'Конец периода'}))
    agent = forms.ModelChoiceField(queryset=Agent.objects.all(), required=False, widget=forms.FilteringSelect())
    brick = forms.ModelChoiceField(queryset=Brick.objects.all(), widget=BrickSelect, required=False)

    def __init__(self, *args, **kwargs):
        """
        Изменение пустой ичейки для подсказки.
        """
        super(Bills, self).__init__(*args, **kwargs)
        self.fields['agent'].empty_label = u'Выберите контрагента'
    class Media:
        js = ('bills.js',)
        css = {'all': ('bills.css',), }