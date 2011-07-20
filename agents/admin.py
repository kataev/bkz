# -*- coding: utf-8 -*-
from django.contrib import admin
from whs.agents.models import agent


class agentAdmin(admin.ModelAdmin):
    list_display = ('name', 'form', 'address', 'phone','id')
    list_filter = ('form','type')
    ordering = ('name','id',)

admin.site.register(agent, agentAdmin)

