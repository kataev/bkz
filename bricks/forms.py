# -*- coding: utf-8 -*-
import dojango.forms as forms

from whs.bricks.models import bricks,history

class brickForm(ModelForm):
    class Meta:
        model=bricks

class brickSelectForm(ModelForm):
    class Meta:
        model=bricks
        exclude = ['total','name','features','color_type','refuse']
        widgets = {
            'color': RadioSelect(),
            'brick_class': RadioSelect(),
            'mark': RadioSelect(),
            'view': RadioSelect(),
            'weight': RadioSelect(),
            'defect': RadioSelect(),
        }