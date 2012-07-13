# -*- coding: utf-8 -*-
from django.contrib import admin
import django.contrib.admin

__author__ = 'bteam'

class AddAdmin(admin.ModelAdmin):
    pass


class ManAdmin(admin.ModelAdmin):
    pass


class BrickAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','name','css','total')