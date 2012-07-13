# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('man_write_off','whs_write_off')
        db.rename_table('man_add','whs_add')
        db.rename_table('man_sorting','whs_sorting')
        db.rename_table('man_sorted','whs_sorted')
        db.rename_table('man_inventory','whs_inventory')
        db.rename_table('man_man','whs_man')
    def backwards(self, orm):
        pass
    models= {}

    complete_apps = ['whs']