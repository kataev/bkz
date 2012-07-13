# -*- coding: utf-8 -*-
__author__ = 'bteam'

from django.contrib import admin
from bkz.brick.models import *

class BrickAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','name','css','total')


admin.site.register(Brick,BrickAdmin)
