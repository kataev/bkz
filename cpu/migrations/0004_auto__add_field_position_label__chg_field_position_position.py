# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Position.label'
        db.add_column('cpu_position', 'label',
                      self.gf('django.db.models.fields.CharField')(default=u'', max_length=50),
                      keep_default=False)


        # Changing field 'Position.position'
        db.alter_column('cpu_position', 'position', self.gf('django.db.models.fields.FloatField')(max_length=100))
    def backwards(self, orm):
        # Deleting field 'Position.label'
        db.delete_column('cpu_position', 'label')


        # Changing field 'Position.position'
        db.alter_column('cpu_position', 'position', self.gf('django.db.models.fields.CharField')(max_length=100))
    models = {
        'cpu.device': {
            'Meta': {'object_name': 'Device'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'cpu.position': {
            'Meta': {'object_name': 'Position'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cpu.Device']"}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.FloatField', [], {'max_length': '100'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cpu']