# -*- coding: utf-8 -*-
from django.contrib import admin
from lab.models import *
__author__ = 'bteam'

class CauseAdmin(admin.ModelAdmin):
    pass

admin.site.register(Cause,CauseAdmin)