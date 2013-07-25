# -*- coding: utf-8 -*-
from django.contrib import admin
from energy.models import *


class EnergyAdmin(admin.ModelAdmin):
    pass


class TeploAdmin(admin.ModelAdmin):
    pass


admin.site.register(Energy, EnergyAdmin)
admin.site.register(Teplo, TeploAdmin)
