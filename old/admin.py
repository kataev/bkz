# -*- coding: utf-8 -*-
__author__ = 'bteam'

from django.contrib import admin
from whs.old.models import *

class TovarAdmin(admin.ModelAdmin):
    list_display = ('prim','total')

class JurnalAdmin(admin.ModelAdmin):
    list_display = ('tov','date','plus','minus','makt','pakt')

class ScladAdmin(admin.ModelAdmin):
    pass

class AgentAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Tovar,TovarAdmin)
admin.site.register(Sclad,ScladAdmin)
admin.site.register(Jurnal,JurnalAdmin)
admin.site.register(Agent,AgentAdmin)
