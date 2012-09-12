# -*- coding: utf-8 -*-
from django.contrib import admin
from whs.models import *
__author__ = 'bteam'

class FeaturesAdmin(admin.ModelAdmin):
    pass

class BrickAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','name','css','total')

admin.site.register(Features,FeaturesAdmin)
admin.site.register(Brick,BrickAdmin)