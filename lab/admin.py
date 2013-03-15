# -*- coding: utf-8 -*-
from django.contrib import admin
from lab.models import *


class CauseAdmin(admin.ModelAdmin):
    pass

class MatherialAdmin(admin.ModelAdmin):
    pass

class BarAdmin(admin.ModelAdmin):
    pass

class RawAdmin(admin.ModelAdmin):
    pass

class HalfAdmin(admin.ModelAdmin):
    pass

class WaterAbsorptionAdmin(admin.ModelAdmin):
    pass

class EfflorescenceAdmin(admin.ModelAdmin):
    pass

class FrostResistanceAdmin(admin.ModelAdmin):
    pass

class SEONRAdmin(admin.ModelAdmin):
    pass

class HeatConductionAdmin(admin.ModelAdmin):
    pass

class BatchAdmin(admin.ModelAdmin):
    pass

class PartAdmin(admin.ModelAdmin):
    pass

class RowPartAdmin(admin.ModelAdmin):
    pass

class TestAdmin(admin.ModelAdmin):
    pass


admin.site.register(Cause,CauseAdmin)
admin.site.register(Matherial,MatherialAdmin)
admin.site.register(Bar,BarAdmin)
admin.site.register(Raw,RawAdmin)
admin.site.register(Half,HalfAdmin)
admin.site.register(WaterAbsorption,WaterAbsorptionAdmin)
admin.site.register(Efflorescence,EfflorescenceAdmin)
admin.site.register(FrostResistance,FrostResistanceAdmin)
admin.site.register(SEONR,SEONRAdmin)
admin.site.register(HeatConduction,HeatConductionAdmin)
admin.site.register(Batch,BatchAdmin)
admin.site.register(Part,PartAdmin)
admin.site.register(RowPart,RowPartAdmin)
admin.site.register(Test,TestAdmin)
