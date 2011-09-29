# -*- coding: utf-8 -*-
import dojango.forms as forms

from whs.brick.models import Brick

class BrickForm(forms.ModelForm):
    class Meta:
        model=Brick
        exclude = ('total',)
    class Media:
        js = ('js/form/Form.js',)
        css = {'all':('css/form.css',),}

class CheckBoxBrickSelect(forms.CheckboxSelectMultiple):
    dojo_type = 'whs.CheckBox'

class BrickFilterForm(forms.ModelForm):
    class Meta:
        model=Brick
        fields = ('mark','brick_class','view','weight','color_type')
        widgets = {
         'mark': CheckBoxBrickSelect(),
         'brick_class': CheckBoxBrickSelect(),
         'view': CheckBoxBrickSelect(),
         'weight': CheckBoxBrickSelect(),
         'color_type': CheckBoxBrickSelect(),
         }
    class Media:
        js = ('bricks.js',)
        css = {'all':('bricks.css',),}