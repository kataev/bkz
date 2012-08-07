# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SEONR.width'
        db.delete_column('lab_seonr', 'width')


        # Changing field 'Part.tto'
        db.alter_column('lab_part', 'tto', self.gf('bkz.lab.models.RangeField')(max_length=30))
    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'SEONR.width'
        raise RuntimeError("Cannot reverse this migration. 'SEONR.width' and its values cannot be restored.")

        # Changing field 'Part.tto'
        db.alter_column('lab_part', 'tto', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=30))
    models = {
        'lab.bar': {
            'Meta': {'object_name': 'Bar'},
            'cutter': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '3000'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 7, 16, 30, 28, 1)'}),
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
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 7, 0, 0)'}),
            'efflorescence': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.Efflorescence']", 'null': 'True', 'blank': 'True'}),
            'flexion': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'frost_resistance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.FrostResistance']", 'null': 'True', 'blank': 'True'}),
            'heatconduction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.HeatConduction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'mark': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pressure': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'seonr': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.SEONR']"}),
            'tto': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'water_absorption': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.WaterAbsorption']", 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.FloatField', [], {'max_length': '30'})
        },
        'lab.clay': {
            'Meta': {'object_name': 'Clay'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 7, 16, 30, 28, 1)'}),
            'dust': ('django.db.models.fields.FloatField', [], {}),
            'humidity': ('bkz.lab.models.SlashSeparatedFloatField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusion': ('django.db.models.fields.FloatField', [], {}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'sand': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.density': {
            'Meta': {'object_name': 'Density'},
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 7, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.efflorescence': {
            'Meta': {'object_name': 'Efflorescence'},
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 7, 0, 0)'}),
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
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 7, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.half': {
            'Meta': {'object_name': 'Half'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 7, 16, 30, 28, 1)'}),
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
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 7, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.part': {
            'Meta': {'object_name': 'Part'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.Batch']"}),
            'brocken': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cause': ('django.db.models.fields.TextField', [], {'max_length': '600', 'blank': 'True'}),
            'defect': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '60', 'blank': 'True'}),
            'dnumber': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'half': ('django.db.models.fields.FloatField', [], {'default': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'test': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tto': ('bkz.lab.models.RangeField', [], {'max_length': '30'})
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
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 7, 16, 30, 28, 1)'}),
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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 7, 0, 0)'}),
            'dirt': ('django.db.models.fields.TextField', [], {}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'module_size': ('django.db.models.fields.FloatField', [], {}),
            'particle_size': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.seonr': {
            'Meta': {'object_name': 'SEONR'},
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 7, 0, 0)'}),
            'delta': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.storedclay': {
            'Meta': {'object_name': 'StoredClay'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 7, 16, 30, 28, 1)'}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'lab.waterabsorption': {
            'Meta': {'object_name': 'WaterAbsorption'},
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 7, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['lab']