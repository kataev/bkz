# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Devices'
        db.create_table('cpu_devices', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('cpu', ['Devices'])

        # Adding model 'Positions'
        db.create_table('cpu_positions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cpu.Devices'])),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('cpu', ['Positions'])

    def backwards(self, orm):
        # Deleting model 'Devices'
        db.delete_table('cpu_devices')

        # Deleting model 'Positions'
        db.delete_table('cpu_positions')

    models = {
        'cpu.devices': {
            'Meta': {'object_name': 'Devices'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'cpu.positions': {
            'Meta': {'object_name': 'Positions'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cpu.Devices']"}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cpu']