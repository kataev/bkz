# -*- coding: utf-8 -*-
import dojango.forms as forms

from whs.brick.models import Brick,History

class BrickForm(forms.ModelForm):
    class Meta:
        model=Brick
        exclude = ('total',)
        widgets = {
#         'mark': forms.CheckboxSelectMultiple(attrs={}),
         }
    class Media:
        js = ('form.js',)
        css = {'all':('form.css',),}


class BrickFilterForm(forms.ModelForm):
    class Meta:
        model=Brick
        fields = ('mark','brick_class','view','weight','color_type')
        widgets = {
         'mark': forms.CheckboxSelectMultiple(),
         'brick_class': forms.CheckboxSelectMultiple(),
         'view': forms.CheckboxSelectMultiple(),
         'weight': forms.CheckboxSelectMultiple(),
         'color_type': forms.CheckboxSelectMultiple(),
         }
#    class Media:
#        js = ('form.js',)
#        css = {'all':('form.css',),}