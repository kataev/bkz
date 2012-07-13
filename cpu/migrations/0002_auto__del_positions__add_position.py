# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Positions'
        db.delete_table('cpu_positions')

        # Adding model 'Position'
        db.create_table('cpu_position', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cpu.Devices'])),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('cpu', ['Position'])

    def backwards(self, orm):
        # Adding model 'Positions'
        db.create_table('cpu_positions', (
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cpu.Devices'])),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('cpu', ['Positions'])

        # Deleting model 'Position'
        db.delete_table('cpu_position')

    models = {
        'cpu.devices': {
            'Meta': {'object_name': 'Devices'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'cpu.position': {
            'Meta': {'object_name': 'Position'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cpu.Devices']"}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cpu']