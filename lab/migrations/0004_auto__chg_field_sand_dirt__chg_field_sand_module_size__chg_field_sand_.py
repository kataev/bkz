# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Sand.dirt'
        db.alter_column('lab_sand', 'dirt', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Sand.module_size'
        db.alter_column('lab_sand', 'module_size', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Sand.particle_size'
        db.alter_column('lab_sand', 'particle_size', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Bar.humidity_transporter'
        db.alter_column('lab_bar', 'humidity_transporter', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Clay.inclusion'
        db.alter_column('lab_clay', 'inclusion', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Clay.humidity'
        db.execute('ALTER TABLE "lab_clay" ALTER "humidity" SET DATA TYPE numeric(10,2) USING humidity::numeric(10,2);')
        db.alter_column('lab_clay', 'humidity', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'Clay.sand'
        db.alter_column('lab_clay', 'sand', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Clay.dust'
        db.alter_column('lab_clay', 'dust', self.gf('django.db.models.fields.FloatField')(null=True))
    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Sand.dirt'
        raise RuntimeError("Cannot reverse this migration. 'Sand.dirt' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Sand.module_size'
        raise RuntimeError("Cannot reverse this migration. 'Sand.module_size' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Sand.particle_size'
        raise RuntimeError("Cannot reverse this migration. 'Sand.particle_size' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Bar.humidity_transporter'
        raise RuntimeError("Cannot reverse this migration. 'Bar.humidity_transporter' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clay.inclusion'
        raise RuntimeError("Cannot reverse this migration. 'Clay.inclusion' and its values cannot be restored.")

        # Changing field 'Clay.humidity'
        db.alter_column('lab_clay', 'humidity', self.gf('bkz.lab.models.SlashSeparatedFloatField')(max_length=300))

        # User chose to not deal with backwards NULL issues for 'Clay.sand'
        raise RuntimeError("Cannot reverse this migration. 'Clay.sand' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Clay.dust'
        raise RuntimeError("Cannot reverse this migration. 'Clay.dust' and its values cannot be restored.")
    models = {
        'lab.bar': {
            'Meta': {'ordering': "('datetime',)", 'object_name': 'Bar'},
            'cavitation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cutter': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '3000'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 11, 0, 0)'}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'humidity_transporter': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
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
            'width': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['whs.Width']"})
        },
        'lab.batch': {
            'Meta': {'ordering': "('-date', '-number')", 'object_name': 'Batch'},
            'amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cad': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'cavitation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'chamfer': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ctype': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '6'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 11, 0, 0)'}),
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
            'weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['whs.Width']"})
        },
        'lab.cause': {
            'Meta': {'ordering': "('type',)", 'object_name': 'Cause'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'lab.clay': {
            'Meta': {'ordering': "('datetime',)", 'object_name': 'Clay'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 11, 0, 0)'}),
            'dust': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusion': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'sand': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'lab.efflorescence': {
            'Meta': {'object_name': 'Efflorescence'},
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 11, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'})
        },
        'lab.frostresistance': {
            'Meta': {'object_name': 'FrostResistance'},
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 11, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'mark': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'value': ('django.db.models.fields.IntegerField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {'default': '0.8', 'max_length': '30'})
        },
        'lab.half': {
            'Meta': {'ordering': "('datetime', '-path', '-position')", 'object_name': 'Half'},
            'cavitation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 11, 0, 0)'}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.IntegerField', [], {}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'shrink': ('django.db.models.fields.FloatField', [], {}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'tts': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'weight': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['whs.Width']"})
        },
        'lab.heatconduction': {
            'Meta': {'object_name': 'HeatConduction'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 11, 0, 0)'}),
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
        'lab.raw': {
            'Meta': {'ordering': "('datetime',)", 'object_name': 'Raw'},
            'cavitation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 11, 0, 0)'}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'temperature': ('django.db.models.fields.FloatField', [], {}),
            'tts': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'weight': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['whs.Width']"})
        },
        'lab.rowpart': {
            'Meta': {'object_name': 'RowPart'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'brocken': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'part': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': "orm['lab.Part']"}),
            'test': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tto': ('bkz.lab.models.RangeField', [], {'max_length': '30'})
        },
        'lab.sand': {
            'Meta': {'ordering': "('datetime',)", 'object_name': 'Sand'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 11, 0, 0)'}),
            'dirt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'module_size': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'particle_size': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'lab.seonr': {
            'Meta': {'object_name': 'SEONR'},
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 11, 0, 0)'}),
            'delta': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.storedclay': {
            'Meta': {'ordering': "('datetime', '-position')", 'object_name': 'StoredClay'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 11, 0, 0)'}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'used': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 11, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {'default': '0.8', 'max_length': '30'})
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
            'width': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['whs.Width']"}),
            'ww': ('django.db.models.fields.FloatField', [], {'default': '1.4'})
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

    complete_apps = ['lab']