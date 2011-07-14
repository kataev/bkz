# -*- coding: utf-8 -*-
from django.contrib import admin
from whs.bills.models import *

class billAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','doc_date')
    list_filter = ('solds__brick','agent')
    ordering = ('-doc_date','agent')

class soldAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','brick','amount','tara','price')
    list_filter = ('brick',)

class transferAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','brick','amount',)

admin.site.register(sold, soldAdmin)
admin.site.register(bill, billAdmin)
admin.site.register(transfer, transferAdmin)