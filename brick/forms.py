# -*- coding: utf-8 -*-
import dojango.forms as forms

from whs.brick.models import Brick,History

class brickForm(ModelForm):
    class Meta:
        model=Brick

class brickSelectForm(ModelForm):
    class Meta:
        model=Brick
        exclude = ['total','name','features','color_type','refuse']
        widgets = {
            'color': RadioSelect(),
            'brick_class': RadioSelect(),
            'mark': RadioSelect(),
            'view': RadioSelect(),
            'weight': RadioSelect(),
            'defect': RadioSelect(),
        }