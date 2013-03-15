# -*- coding: utf-8 -*-
from django.contrib import admin
from cpu.models import *


class CpuDeviceAdmin(admin.ModelAdmin):
    pass

class PositionAdmin(admin.ModelAdmin):
    pass

class ValueAdmin(admin.ModelAdmin):
    pass


admin.site.register(CpuDevice,CpuDeviceAdmin)
admin.site.register(Position,PositionAdmin)
admin.site.register(Value,ValueAdmin)
