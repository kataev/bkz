# -*- coding: utf-8 -*-
from django.contrib import admin
from old.models import *


class DispAgentAdmin(admin.ModelAdmin):
    pass


class DispJurnalAdmin(admin.ModelAdmin):
    pass


class DispScladAdmin(admin.ModelAdmin):
    pass


class DispTovarAdmin(admin.ModelAdmin):
    pass


admin.site.register(DispAgent, DispAgentAdmin)
admin.site.register(DispJurnal, DispJurnalAdmin)
admin.site.register(DispSclad, DispScladAdmin)
admin.site.register(DispTovar, DispTovarAdmin)
