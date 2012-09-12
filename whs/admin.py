# -*- coding: utf-8 -*-
from django.contrib import admin

__author__ = 'bteam'

class AddAdmin(admin.ModelAdmin):
    pass


class BrickAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','name','css','total')