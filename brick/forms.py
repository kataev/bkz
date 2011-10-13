# -*- coding: utf-8 -*-
import dojango.forms as forms
from whs.brick.models import Brick

class BrickForm(forms.ModelForm):
    class Meta:
        model=Brick
        exclude = ('total','css','label')
    class Media:
        js = ('js/form.js',)
        css = {'all':('css/form.css',),}

class CheckBoxBrickSelect(forms.CheckboxSelectMultiple):
    dojo_type = 'whs.form.CheckBox'

class BrickFilterForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(BrickFilterForm,self).__init__(*args,**kwargs)
        for k,w in self.fields.iteritems():
            q = w.choices
            choice = []
            for item in q:
                if not item[0] == '': choice.append([Brick.css_dict[k][item[0]],item[1][:7]])
            w.choices = choice

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
        js = ('js/bricks.js',)
        css = {'all':('css/bricks.css',),}