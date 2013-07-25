# -*- coding: utf-8 -*-
from django.contrib import admin
from it.models import *


class DeviceAdmin(admin.ModelAdmin):
    pass


class BuyAdmin(admin.ModelAdmin):
    pass


class PlugAdmin(admin.ModelAdmin):
    pass


admin.site.register(Device, DeviceAdmin)
admin.site.register(Buy, BuyAdmin)
admin.site.register(Plug, PlugAdmin)
