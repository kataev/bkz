# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Bar.width'
        db.alter_column('lab_bar', 'width', self.gf('django.db.models.fields.CharField')(max_length=30))
    def backwards(self, orm):

        # Changing field 'Bar.width'
        db.alter_column('lab_bar', 'width', self.gf('django.db.models.fields.CharField')(max_length=300))
    models = {
        'lab.bar': {
            'Meta': {'object_name': 'Bar'},
            'cutter': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '3000'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 11, 14, 52, 44, 2)'}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'humidity_transporter': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'poke_left': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '300'}),
            'poke_right': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '300'}),
            'sand': ('django.db.models.fields.FloatField', [], {}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'stratcher_left': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '300'}),
            'stratcher_right': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '300'}),
            'temperature': ('django.db.models.fields.FloatField', [], {}),
            'tts': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'weight': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.CharField', [], {'default': '1.0', 'max_length': '30'})
        },
        'lab.batch': {
            'Meta': {'object_name': 'Batch'},
            'chamfer': ('django.db.models.fields.IntegerField', [], {'max_length': '300'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 11, 0, 0)'}),
            'density': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.Density']"}),
            'efflorescence': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.Efflorescence']", 'null': 'True', 'blank': 'True'}),
            'frost_resistance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.FrostResistance']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusion': ('django.db.models.fields.TextField', [], {}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'mark': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tto': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'water_absorption': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.WaterAbsorption']", 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'lab.clay': {
            'Meta': {'object_name': 'Clay'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 11, 14, 52, 44, 2)'}),
            'dust': ('django.db.models.fields.FloatField', [], {}),
            'humidity': ('whs.lab.models.SlashSeparatedFloatField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusion': ('django.db.models.fields.FloatField', [], {}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'sand': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.density': {
            'Meta': {'object_name': 'Density'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 11, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'lab.efflorescence': {
            'Meta': {'object_name': 'Efflorescence'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 11, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.flexion': {
            'Meta': {'object_name': 'Flexion'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.Batch']"}),
            'concavity': ('django.db.models.fields.FloatField', [], {}),
            'flatness': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'perpendicularity': ('django.db.models.fields.FloatField', [], {}),
            'row': ('django.db.models.fields.IntegerField', [], {}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tto': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.frostresistance': {
            'Meta': {'object_name': 'FrostResistance'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 11, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'lab.half': {
            'Meta': {'object_name': 'Half'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 11, 14, 52, 44, 2)'}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.IntegerField', [], {}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'shrink': ('django.db.models.fields.FloatField', [], {}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'weight': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'lab.part': {
            'Meta': {'object_name': 'Part'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.Batch']"}),
            'cause': ('django.db.models.fields.TextField', [], {'max_length': '600'}),
            'defect': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'tto': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '30'})
        },
        'lab.pressure': {
            'Meta': {'object_name': 'Pressure'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.Batch']"}),
            'concavity': ('django.db.models.fields.FloatField', [], {}),
            'flatness': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'perpendicularity': ('django.db.models.fields.FloatField', [], {}),
            'row': ('django.db.models.fields.IntegerField', [], {}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tto': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.raw': {
            'Meta': {'object_name': 'Raw'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 11, 14, 52, 44, 2)'}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'temperature': ('django.db.models.fields.FloatField', [], {}),
            'tts': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'weight': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.sand': {
            'Meta': {'object_name': 'Sand'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 11, 0, 0)'}),
            'dirt': ('django.db.models.fields.TextField', [], {}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'module_size': ('django.db.models.fields.FloatField', [], {}),
            'particle_size': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.storedclay': {
            'Meta': {'object_name': 'StoredClay'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 11, 14, 52, 44, 2)'}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'default': '1', 'max_length': '30'})
        },
        'lab.waterabsorption': {
            'Meta': {'object_name': 'WaterAbsorption'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 11, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['lab']