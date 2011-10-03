# -*- coding: utf-8 -*-
__author__ = 'bteam'

from django.contrib import admin
from whs.bill.models import *

class BillAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','date','agent')
    list_filter = ('date','agent',)

class SoldAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','amount','doc')
    list_filter = ('brick','amount',)

admin.site.register(Bill,BillAdmin)
admin.site.register(Sold,SoldAdmin)
