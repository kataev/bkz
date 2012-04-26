# -*- coding: utf-8 -*-
__author__ = 'bteam'

from django.contrib import admin
from whs.man.models import *

class ManAdmin(admin.ModelAdmin):
    pass

class AddAdmin(admin.ModelAdmin):
    pass

admin.site.register(Man,ManAdmin)
admin.site.register(Add,AddAdmin)
