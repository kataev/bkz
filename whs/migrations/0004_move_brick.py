# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('brick_brick','whs_brick')
        db.rename_table('brick_oldbrick','whs_oldbrick')

    def backwards(self, orm):
        pass
        
    models = {}
    complete_apps = ['whs']