# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
#        db.create_table('whs_price')
#        db.rename_table('sale_sold','whs_sold')
#        db.rename_table('sale_pallet','whs_pallet')
#        db.rename_table('sale_agent','whs_agent')
#        db.rename_table('sale_nomenclature','whs_nomenclature')
#        db.rename_table('sale_seller','whs_seller')
#        db.rename_table('sale_buhagent','whs_buhagent')
#        db.rename_table('sale_oldagent','whs_oldagent')
#        db.rename_table('sale_bill','whs_bill')
        pass
#        if not db.dry_run:
#            orm['contenttypes.contenttype'].objects.filter(app_label='sale').update(app_label='whs')

    def backwards(self, orm):
        pass
    models = {

    }    
    complete_apps = ['whs']
