# -*- coding: utf-8 -*-
from django.contrib import admin
from whs.bricks.models import bricks


class bricksAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','get_mark_display','get_view_display','get_weight_display','total','id')
#    ordering = ('brick_class','-weight','-view','color_type','defect','refuse','mark','features','color')
    list_filter = ('brick_class','weight','view','defect','refuse','mark')

admin.site.register(bricks, bricksAdmin)

