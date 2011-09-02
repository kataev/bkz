# -*- coding: utf-8 -*-
from django.contrib import admin
from whs.agent.models import Agent


class agentAdmin(admin.ModelAdmin):
    list_display = ('name', 'form', 'address', 'phone','id')
    list_filter = ('form','type')
    ordering = ('name','id',)

admin.site.register(Agent, agentAdmin)

