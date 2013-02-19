# -*- coding: utf-8 -*-
from django.contrib import admin
from bkz.cpu.models import CpuDevice, Position

class CpuDeviceAdmin(admin.ModelAdmin):
	pass

admin.site.register(CpuDevice,CpuDeviceAdmin)

class PositionAdmin(admin.ModelAdmin):
	pass

admin.site.register(Position,PositionAdmin)