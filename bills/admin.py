# -*- coding: utf-8 -*-
from django.contrib import admin
from whs.bills.models import *

class billAdmin(admin.ModelAdmin):
    pass

class soldAdmin(admin.ModelAdmin):
    pass

class transferAdmin(admin.ModelAdmin):
    pass

admin.site.register(sold, soldAdmin)
admin.site.register(bill, billAdmin)
admin.site.register(transfer, transferAdmin)