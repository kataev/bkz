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

class CheckboxBrickSelect(forms.CheckboxSelectMultiple):
    dojo_type = 'whs.Checkbox'

class BrickFilterForm(forms.ModelForm):
    class Meta:
        model=Brick
        fields = ('mark','brick_class','view','weight','color_type')
        widgets = {
         'mark': CheckboxBrickSelect(),
         'brick_class': CheckboxBrickSelect(),
         'view': CheckboxBrickSelect(),
         'weight': CheckboxBrickSelect(),
         'color_type': CheckboxBrickSelect(),
         }
#    class Media:
#        js = ('form.js',)
#        css = {'all':('form.css',),}