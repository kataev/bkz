# -*- coding: utf-8 -*-
from django.contrib import admin
from make.models import *


class FormingAdmin(admin.ModelAdmin):
    pass

class WarrenAdmin(admin.ModelAdmin):
    pass


admin.site.register(Forming,FormingAdmin)
admin.site.register(Warren,WarrenAdmin)
