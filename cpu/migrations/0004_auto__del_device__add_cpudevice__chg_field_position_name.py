# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Device'
        db.delete_table('cpu_device')

        # Adding model 'CpuDevice'
        db.create_table('cpu_cpudevice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('cpu', ['CpuDevice'])


        # Changing field 'Position.name'
        db.alter_column('cpu_position', 'name_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cpu.CpuDevice']))
    def backwards(self, orm):
        # Adding model 'Device'
        db.create_table('cpu_device', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('cpu', ['Device'])

        # Deleting model 'CpuDevice'
        db.delete_table('cpu_cpudevice')


        # Changing field 'Position.name'
        db.alter_column('cpu_position', 'name_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cpu.Device']))
    models = {
        'cpu.cpudevice': {
            'Meta': {'object_name': 'CpuDevice'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'cpu.position': {
            'Meta': {'object_name': 'Position'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cpu.CpuDevice']"}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.FloatField', [], {'max_length': '100'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'cpu.value': {
            'Meta': {'object_name': 'Value'},
            'code': ('django.db.models.fields.IntegerField', [], {}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'field': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['cpu']