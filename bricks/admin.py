# -*- coding: utf-8 -*-
from django.contrib import admin
from whs.bricks.models import bricks


class bricksAdmin(admin.ModelAdmin):
    pass

admin.site.register(bricks, bricksAdmin)

