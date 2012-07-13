# -*- coding: utf-8 -*-
__author__ = 'bteam'
from django.contrib import admin
from bkz.ipaccess.models import IPAccess

class IpAdmin(admin.ModelAdmin):
    list_display = ('user','ip')

admin.site.register(IPAccess,IpAdmin)
