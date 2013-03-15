# -*- coding: utf-8 -*-
from django.contrib import admin
from whs.models import *


class WidthAdmin(admin.ModelAdmin):
    pass

class FeaturesAdmin(admin.ModelAdmin):
    pass

class BrickAdmin(admin.ModelAdmin):
    pass

class OldBrickAdmin(admin.ModelAdmin):
    pass

class AgentAdmin(admin.ModelAdmin):
    pass

class SellerAdmin(admin.ModelAdmin):
    pass

class OldAgentAdmin(admin.ModelAdmin):
    pass

class BillAdmin(admin.ModelAdmin):
    pass

class PalletAdmin(admin.ModelAdmin):
    pass

class SoldAdmin(admin.ModelAdmin):
    pass

class NomenclatureAdmin(admin.ModelAdmin):
    pass

class BuhAgentAdmin(admin.ModelAdmin):
    pass

class SortingAdmin(admin.ModelAdmin):
    pass

class InventoryAdmin(admin.ModelAdmin):
    pass

class Write_offAdmin(admin.ModelAdmin):
    pass


admin.site.register(Width,WidthAdmin)
admin.site.register(Features,FeaturesAdmin)
admin.site.register(Brick,BrickAdmin)
admin.site.register(OldBrick,OldBrickAdmin)
admin.site.register(Agent,AgentAdmin)
admin.site.register(Seller,SellerAdmin)
admin.site.register(OldAgent,OldAgentAdmin)
admin.site.register(Bill,BillAdmin)
admin.site.register(Pallet,PalletAdmin)
admin.site.register(Sold,SoldAdmin)
admin.site.register(Nomenclature,NomenclatureAdmin)
admin.site.register(BuhAgent,BuhAgentAdmin)
admin.site.register(Sorting,SortingAdmin)
admin.site.register(Inventory,InventoryAdmin)
admin.site.register(Write_off,Write_offAdmin)
