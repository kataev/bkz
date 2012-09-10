# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Part.sorted'
        db.add_column('lab_part', 'sorted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Part.sorted'
        db.delete_column('lab_part', 'sorted')

    models = {
        'lab.bar': {
            'Meta': {'object_name': 'Bar'},
            'cutter': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '3000'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 29, 15, 10, 18, 2)'}),
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
            'amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'chamfer': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 29, 0, 0)'}),
            'density': ('django.db.models.fields.FloatField', [], {}),
            'flexion': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'frost_resistance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.FrostResistance']", 'null': 'True', 'blank': 'True'}),
            'heatconduction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.HeatConduction']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'mark': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pressure': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'seonr': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.SEONR']", 'null': 'True', 'blank': 'True'}),
            'tto': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'water_absorption': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.WaterAbsorption']", 'null': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {'default': '0.8', 'max_length': '30'})
        },
        'lab.clay': {
            'Meta': {'object_name': 'Clay'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 29, 15, 10, 18, 2)'}),
            'dust': ('django.db.models.fields.FloatField', [], {}),
            'humidity': ('bkz.lab.models.SlashSeparatedFloatField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusion': ('django.db.models.fields.FloatField', [], {}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'sand': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.density': {
            'Meta': {'object_name': 'Density'},
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 29, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {'default': '0.8', 'max_length': '30'})
        },
        'lab.efflorescence': {
            'Meta': {'object_name': 'Efflorescence'},
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 29, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'})
        },
        'lab.flexion': {
            'Meta': {'object_name': 'Flexion'},
            'area': ('django.db.models.fields.FloatField', [], {}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'flexion_tests'", 'to': "orm['lab.Batch']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'readings': ('django.db.models.fields.FloatField', [], {}),
            'row': ('django.db.models.fields.IntegerField', [], {}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tto': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        'lab.frostresistance': {
            'Meta': {'object_name': 'FrostResistance'},
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 29, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'mark': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {'default': '0.8', 'max_length': '30'})
        },
        'lab.half': {
            'Meta': {'object_name': 'Half'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 29, 15, 10, 18, 2)'}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.IntegerField', [], {}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'shrink': ('django.db.models.fields.FloatField', [], {}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'weight': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.heatconduction': {
            'Meta': {'object_name': 'HeatConduction'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 29, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {'default': '0.8', 'max_length': '30'})
        },
        'lab.part': {
            'Meta': {'object_name': 'Part'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.Batch']"}),
            'brocken': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cause': ('django.db.models.fields.TextField', [], {'max_length': '600', 'blank': 'True'}),
            'defect': ('django.db.models.fields.CharField', [], {'default': "u' '", 'max_length': '60'}),
            'dnumber': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'half': ('django.db.models.fields.FloatField', [], {'default': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'sorted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'test': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tto': ('bkz.lab.models.RangeField', [], {'max_length': '30', 'blank': 'True'})
        },
        'lab.pressure': {
            'Meta': {'object_name': 'Pressure'},
            'area': ('django.db.models.fields.FloatField', [], {}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'pressure_tests'", 'to': "orm['lab.Batch']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'readings': ('django.db.models.fields.FloatField', [], {}),
            'row': ('django.db.models.fields.IntegerField', [], {}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tto': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        'lab.raw': {
            'Meta': {'object_name': 'Raw'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 29, 15, 10, 18, 2)'}),
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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 29, 0, 0)'}),
            'dirt': ('django.db.models.fields.TextField', [], {}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'module_size': ('django.db.models.fields.FloatField', [], {}),
            'particle_size': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.seonr': {
            'Meta': {'object_name': 'SEONR'},
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 29, 0, 0)'}),
            'delta': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.storedclay': {
            'Meta': {'object_name': 'StoredClay'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 29, 15, 10, 18, 2)'}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'lab.waterabsorption': {
            'Meta': {'object_name': 'WaterAbsorption'},
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 29, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {'default': '0.8', 'max_length': '30'})
        }
    }

    complete_apps = ['lab']