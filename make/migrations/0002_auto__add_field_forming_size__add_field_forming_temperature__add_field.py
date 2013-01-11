# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Forming.size'
        db.add_column('make_forming', 'size',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20),
                      keep_default=False)

        # Adding field 'Forming.temperature'
        db.add_column('make_forming', 'temperature',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Forming.humidity'
        db.add_column('make_forming', 'humidity',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Forming.vacuum'
        db.add_column('make_forming', 'vacuum',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Forming.size'
        db.delete_column('make_forming', 'size')

        # Deleting field 'Forming.temperature'
        db.delete_column('make_forming', 'temperature')

        # Deleting field 'Forming.humidity'
        db.delete_column('make_forming', 'humidity')

        # Deleting field 'Forming.vacuum'
        db.delete_column('make_forming', 'vacuum')

    models = {
        'make.forming': {
            'Meta': {'object_name': 'Forming'},
            'cavitation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 10, 0, 0)'}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'temperature': ('django.db.models.fields.FloatField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tts': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'vacuum': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['whs.Width']"})
        },
        'make.warren': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Warren'},
            'amount': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 10, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'consumer'", 'null': 'True', 'to': "orm['make.Warren']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'whs.width': {
            'Meta': {'ordering': "('pk',)", 'object_name': 'Width'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'type': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['make']