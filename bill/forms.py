# -*- coding: utf-8 -*-
from whs.bill.models import *

import dojango.forms as forms
from django.utils.encoding import StrAndUnicode, force_unicode
from itertools import chain
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.contrib.humanize.templatetags.humanize import intcomma

class BrickSelect(forms.Select):
    dojo_type = 'whs.brickSelect'

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select%s>' % flatatt(final_attrs)]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append(u'</select>')
        return mark_safe(u'\n'.join(output))

    def render_option(self,brick,selected_choices, option_value=None, option_label=None):
        if brick is None:
            return u''
        else:
            selected_html = (brick.pk in selected_choices) and u' selected="selected"' or ''
            return u'<option dojoType="whs.brick_tr" class="%(class)s" cl="%(cl)s" mark="%(mark)s" view="%(view)s" weight="%(weight)s" total="%(total)s" value="%(pk)s"%(selected_html)s>%(title)s</option>' % {
                'class':brick.show_css(),
                'cl':brick.get_brick_class_display(),
                'mark':brick.get_mark_display(),
                'view':brick.get_view_display(),
                'weight':brick.get_weight_display(),
                'total':intcomma(brick.total),
                'pk':brick.pk,
                'selected_html':selected_html,
                'title':brick

            }

    def render_options(self, choices, selected_choices):
        selected_choices = set([v for v in selected_choices])
        output = []
        br =  self.choices.queryset
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    try:
                        print option_value
                        val = int(option_value)
                        output.append(self.render_option(br.get(pk=val),selected_choices,*option))
                    except ValueError:
                        output.append(self.render_option(None,selected_choices,*option))
                output.append(u'</optgroup>')
            else:
                try:
                    val = br.get(pk=option_value)
                except :
                    val = None
                output.append(self.render_option(val,selected_choices))
        return u'\n'.join(output)

class OperSelect(forms.SelectMultiple):
    dojo_type = 'whs.operSelect'
    def render_option(self,oper,selected_choices):
        selected_html = (oper.pk in selected_choices) and u' selected="selected"' or ''
        return oper.widget(selected_html=selected_html,as_tr=True)

    def render_options(self, choices, selected_choices):
        selected_choices = set([v for v in selected_choices])
        output = []
        queryset =  self.choices.queryset
        for oper in queryset:
            output.append(self.render_option(oper,selected_choices))
        return u'\n'.join(output)

class Form(forms.ModelForm):
    class Media:
        js = ('form.js',)
        css = {'all':('form.css',),}


class SoldForm(Form):
    bill = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model=Sold
        exclude=('post')
        widgets = {
         'info': forms.Textarea(attrs={}),
         'brick': BrickSelect(),
         'tara': forms.NumberSpinnerInput(attrs={'style':'width:90px;','constraints':{'min':1,'max':2000,'places':0}})
         }


class TransferForm(Form):
    bill = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model=Transfer
        exclude=('post')
        widgets = {
         'info': forms.Textarea(attrs={}),
         'brick': BrickSelect(),
         'sold' : forms.HiddenInput()
         }


class BillForm(Form):
    class Meta:
        model=Bill
        exclude=('draft')
        widgets = {
         'info': forms.Textarea(attrs={}),
         'agent' : forms.FilteringSelect(),
         'solds': OperSelect(),
         'transfers': OperSelect()
         }

class Finish_transfer(forms.Form):
    sold = forms.ModelChoiceField(queryset=Sold.objects.all())
    transfer = forms.ModelChoiceField(queryset=Transfer.objects.filter(sold__isnull=True))