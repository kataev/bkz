# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Warren.number'
        db.alter_column('make_warren', 'number', self.gf('django.db.models.fields.CharField')(max_length=5))
    def backwards(self, orm):

        # Changing field 'Warren.number'
        db.alter_column('make_warren', 'number', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=5))
    models = {
        'lab.batch': {
            'Meta': {'ordering': "('-date', '-number')", 'object_name': 'Batch'},
            'amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cad': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'cavitation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'chamfer': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ctype': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '6'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 2, 3, 0, 0)'}),
            'density': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'flexion': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'frost_resistance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.FrostResistance']", 'null': 'True', 'blank': 'True'}),
            'heatconduction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.HeatConduction']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'mark': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pf': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pressure': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'seonr': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.SEONR']", 'null': 'True', 'blank': 'True'}),
            'tto': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'view': ('django.db.models.fields.CharField', [], {'default': "u'\\u041b'", 'max_length': '60'}),
            'volume': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'volume_test'", 'null': 'True', 'to': "orm['lab.Test']"}),
            'water_absorption': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.WaterAbsorption']", 'null': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['whs.Width']"})
        },
        'lab.cause': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Cause'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'part'", 'max_length': '30'})
        },
        'lab.frostresistance': {
            'Meta': {'object_name': 'FrostResistance'},
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 2, 3, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'mark': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'value': ('django.db.models.fields.IntegerField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {'default': '0.8', 'max_length': '30'})
        },
        'lab.heatconduction': {
            'Meta': {'object_name': 'HeatConduction'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 2, 3, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {'default': '0.8', 'max_length': '30'})
        },
        'lab.part': {
            'Meta': {'ordering': "('-batch__date', '-batch__number')", 'object_name': 'Part'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parts'", 'to': "orm['lab.Batch']"}),
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['whs.Brick']", 'null': 'True', 'blank': 'True'}),
            'cause': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lab.Cause']", 'null': 'True', 'blank': 'True'}),
            'defect': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'dnumber': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'half': ('django.db.models.fields.FloatField', [], {'default': '3.0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'limestone': ('bkz.lab.models.RangeField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        'lab.seonr': {
            'Meta': {'object_name': 'SEONR'},
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 2, 3, 0, 0)'}),
            'delta': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.test': {
            'Meta': {'ordering': "('row',)", 'object_name': 'Test'},
            'area': ('django.db.models.fields.FloatField', [], {}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'tests'", 'to': "orm['lab.Batch']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'readings': ('django.db.models.fields.FloatField', [], {}),
            'row': ('django.db.models.fields.IntegerField', [], {}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tto': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        'lab.waterabsorption': {
            'Meta': {'object_name': 'WaterAbsorption'},
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 2, 3, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {'default': '0.8', 'max_length': '30'})
        },
        'make.forming': {
            'Meta': {'ordering': "('date',)", 'unique_together': "(('date', 'tts'),)", 'object_name': 'Forming'},
            'cavitation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 2, 3, 0, 0)'}),
            'density': ('django.db.models.fields.FloatField', [], {}),
            'humidity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'k': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'poke': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'sand': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'stratcher': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'tts': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'vacuum': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['whs.Width']"})
        },
        'make.warren': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Warren'},
            'brocken': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cause': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lab.Cause']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 2, 3, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'forming': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'warrens'", 'null': 'True', 'to': "orm['make.Forming']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'part': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'warrens'", 'null': 'True', 'to': "orm['lab.Part']"}),
            'path': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'consumer'", 'null': 'True', 'to': "orm['make.Warren']"})
        },
        'whs.brick': {
            'Meta': {'ordering': "('width', 'color', '-view', 'ctype', '-defect', '-features__name', 'mark', 'refuse', 'id')", 'object_name': 'Brick'},
            'cad': ('django.db.models.fields.FloatField', [], {}),
            'cavitation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'color': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'css': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '360'}),
            'ctype': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '6', 'blank': 'True'}),
            'defect': ('django.db.models.fields.CharField', [], {'default': "u'gost'", 'max_length': '60', 'blank': 'True'}),
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['whs.Features']", 'null': 'True', 'blank': 'True'}),
            'frost_resistance': ('django.db.models.fields.PositiveIntegerField', [], {'default': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '660'}),
            'mark': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'}),
            'mass': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '160'}),
            'nomenclature': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['whs.Nomenclature']", 'null': 'True', 'blank': 'True'}),
            'refuse': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '10', 'blank': 'True'}),
            'total': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'view': ('django.db.models.fields.CharField', [], {'default': "u'\\u041b'", 'max_length': '60'}),
            'width': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['whs.Width']"})
        },
        'whs.features': {
            'Meta': {'ordering': "('type',)", 'object_name': 'Features'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'whs.nomenclature': {
            'Meta': {'object_name': 'Nomenclature'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
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