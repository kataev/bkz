# -*- coding: utf-8 -*-
from django.contrib import admin
from whs.agents.models import agent


class agentAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'form', 'address', 'phone')
    list_filter = ('form','type')
    ordering = ('id','name')

admin.site.register(agent, agentAdmin)

