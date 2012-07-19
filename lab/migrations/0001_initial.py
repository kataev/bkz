# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Clay'
        db.create_table('lab_clay', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 7, 19, 14, 8, 52, 3))),
            ('humidity', self.gf('bkz.lab.models.SlashSeparatedFloatField')(max_length=300)),
            ('sand', self.gf('django.db.models.fields.FloatField')()),
            ('inclusion', self.gf('django.db.models.fields.FloatField')()),
            ('dust', self.gf('django.db.models.fields.FloatField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['Clay'])

        # Adding model 'StoredClay'
        db.create_table('lab_storedclay', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 7, 19, 14, 8, 52, 3))),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('humidity', self.gf('django.db.models.fields.FloatField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['StoredClay'])

        # Adding model 'Sand'
        db.create_table('lab_sand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 7, 19, 0, 0))),
            ('humidity', self.gf('django.db.models.fields.FloatField')()),
            ('particle_size', self.gf('django.db.models.fields.FloatField')()),
            ('module_size', self.gf('django.db.models.fields.FloatField')()),
            ('dirt', self.gf('django.db.models.fields.TextField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['Sand'])

        # Adding model 'Bar'
        db.create_table('lab_bar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 7, 19, 14, 8, 52, 3))),
            ('width', self.gf('django.db.models.fields.CharField')(default=1.0, max_length=30)),
            ('tts', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('weight', self.gf('django.db.models.fields.FloatField')()),
            ('temperature', self.gf('django.db.models.fields.FloatField')()),
            ('humidity', self.gf('django.db.models.fields.FloatField')()),
            ('sand', self.gf('django.db.models.fields.FloatField')()),
            ('poke_left', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=300)),
            ('poke_right', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=300)),
            ('stratcher_left', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=300)),
            ('stratcher_right', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=300)),
            ('cutter', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=3000)),
            ('humidity_transporter', self.gf('django.db.models.fields.FloatField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000)),
        ))
        db.send_create_signal('lab', ['Bar'])

        # Adding model 'Raw'
        db.create_table('lab_raw', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 7, 19, 14, 8, 52, 3))),
            ('tts', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('temperature', self.gf('django.db.models.fields.FloatField')()),
            ('weight', self.gf('django.db.models.fields.FloatField')()),
            ('humidity', self.gf('django.db.models.fields.FloatField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['Raw'])

        # Adding model 'Half'
        db.create_table('lab_half', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 7, 19, 14, 8, 52, 3))),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('path', self.gf('django.db.models.fields.IntegerField')()),
            ('width', self.gf('django.db.models.fields.FloatField')()),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('weight', self.gf('django.db.models.fields.FloatField')()),
            ('humidity', self.gf('django.db.models.fields.FloatField')()),
            ('shrink', self.gf('django.db.models.fields.FloatField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['Half'])

        # Adding model 'WaterAbsorption'
        db.create_table('lab_waterabsorption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 7, 19, 0, 0))),
            ('width', self.gf('django.db.models.fields.FloatField')()),
            ('color', self.gf('django.db.models.fields.IntegerField')()),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['WaterAbsorption'])

        # Adding model 'Efflorescence'
        db.create_table('lab_efflorescence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 7, 19, 0, 0))),
            ('color', self.gf('django.db.models.fields.IntegerField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['Efflorescence'])

        # Adding model 'FrostResistance'
        db.create_table('lab_frostresistance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 7, 19, 0, 0))),
            ('width', self.gf('django.db.models.fields.FloatField')()),
            ('color', self.gf('django.db.models.fields.IntegerField')()),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['FrostResistance'])

        # Adding model 'Density'
        db.create_table('lab_density', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 7, 19, 0, 0))),
            ('width', self.gf('django.db.models.fields.FloatField')()),
            ('color', self.gf('django.db.models.fields.IntegerField')()),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['Density'])

        # Adding model 'SEONR'
        db.create_table('lab_seonr', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 7, 19, 0, 0))),
            ('width', self.gf('django.db.models.fields.FloatField')()),
            ('color', self.gf('django.db.models.fields.IntegerField')()),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('delta', self.gf('django.db.models.fields.FloatField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['SEONR'])

        # Adding model 'HeatConduction'
        db.create_table('lab_heatconduction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 7, 19, 0, 0))),
            ('width', self.gf('django.db.models.fields.FloatField')()),
            ('color', self.gf('django.db.models.fields.IntegerField')()),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['HeatConduction'])

        # Adding model 'Batch'
        db.create_table('lab_batch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 7, 19, 0, 0))),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('tto', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
            ('width', self.gf('django.db.models.fields.FloatField')(max_length=30)),
            ('color', self.gf('django.db.models.fields.IntegerField')()),
            ('water_absorption', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab.WaterAbsorption'], null=True, blank=True)),
            ('efflorescence', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab.Efflorescence'], null=True, blank=True)),
            ('frost_resistance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab.FrostResistance'], null=True, blank=True)),
            ('seonr', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab.SEONR'])),
            ('heatconduction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab.HeatConduction'])),
            ('inclusion', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pressure', self.gf('django.db.models.fields.FloatField')()),
            ('flexion', self.gf('django.db.models.fields.FloatField')()),
            ('mark', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('chamfer', self.gf('django.db.models.fields.IntegerField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=300, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['Batch'])

        # Adding model 'Pressure'
        db.create_table('lab_pressure', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'pressure_tests', to=orm['lab.Batch'])),
            ('tto', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('row', self.gf('django.db.models.fields.IntegerField')()),
            ('concavity', self.gf('django.db.models.fields.FloatField')()),
            ('perpendicularity', self.gf('django.db.models.fields.FloatField')()),
            ('flatness', self.gf('django.db.models.fields.FloatField')()),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('lab', ['Pressure'])

        # Adding model 'Flexion'
        db.create_table('lab_flexion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'flexion_tests', to=orm['lab.Batch'])),
            ('tto', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('row', self.gf('django.db.models.fields.IntegerField')()),
            ('concavity', self.gf('django.db.models.fields.FloatField')()),
            ('perpendicularity', self.gf('django.db.models.fields.FloatField')()),
            ('flatness', self.gf('django.db.models.fields.FloatField')()),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('lab', ['Flexion'])

        # Adding model 'Part'
        db.create_table('lab_part', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab.Batch'])),
            ('tto', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=30)),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
            ('test', self.gf('django.db.models.fields.IntegerField')()),
            ('half', self.gf('django.db.models.fields.FloatField')()),
            ('defect', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('dnumber', self.gf('django.db.models.fields.FloatField')()),
            ('cause', self.gf('django.db.models.fields.TextField')(max_length=600)),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['Part'])

    def backwards(self, orm):
        # Deleting model 'Clay'
        db.delete_table('lab_clay')

        # Deleting model 'StoredClay'
        db.delete_table('lab_storedclay')

        # Deleting model 'Sand'
        db.delete_table('lab_sand')

        # Deleting model 'Bar'
        db.delete_table('lab_bar')

        # Deleting model 'Raw'
        db.delete_table('lab_raw')

        # Deleting model 'Half'
        db.delete_table('lab_half')

        # Deleting model 'WaterAbsorption'
        db.delete_table('lab_waterabsorption')

        # Deleting model 'Efflorescence'
        db.delete_table('lab_efflorescence')

        # Deleting model 'FrostResistance'
        db.delete_table('lab_frostresistance')

        # Deleting model 'Density'
        db.delete_table('lab_density')

        # Deleting model 'SEONR'
        db.delete_table('lab_seonr')

        # Deleting model 'HeatConduction'
        db.delete_table('lab_heatconduction')

        # Deleting model 'Batch'
        db.delete_table('lab_batch')

        # Deleting model 'Pressure'
        db.delete_table('lab_pressure')

        # Deleting model 'Flexion'
        db.delete_table('lab_flexion')

        # Deleting model 'Part'
        db.delete_table('lab_part')

    models = {
        'lab.bar': {
            'Meta': {'object_name': 'Bar'},
            'cutter': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '3000'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 19, 14, 8, 52, 3)'}),
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
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'chamfer': ('django.db.models.fields.IntegerField', [], {}),
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 19, 0, 0)'}),
            'efflorescence': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.Efflorescence']", 'null': 'True', 'blank': 'True'}),
            'flexion': ('django.db.models.fields.FloatField', [], {}),
            'frost_resistance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.FrostResistance']", 'null': 'True', 'blank': 'True'}),
            'heatconduction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.HeatConduction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'mark': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pressure': ('django.db.models.fields.FloatField', [], {}),
            'seonr': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.SEONR']"}),
            'tto': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'water_absorption': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.WaterAbsorption']", 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.FloatField', [], {'max_length': '30'})
        },
        'lab.clay': {
            'Meta': {'object_name': 'Clay'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 19, 14, 8, 52, 3)'}),
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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 19, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.efflorescence': {
            'Meta': {'object_name': 'Efflorescence'},
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 19, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'})
        },
        'lab.flexion': {
            'Meta': {'object_name': 'Flexion'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'flexion_tests'", 'to': "orm['lab.Batch']"}),
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
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 19, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.half': {
            'Meta': {'object_name': 'Half'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 19, 14, 8, 52, 3)'}),
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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 19, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.part': {
            'Meta': {'object_name': 'Part'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.Batch']"}),
            'cause': ('django.db.models.fields.TextField', [], {'max_length': '600'}),
            'defect': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'dnumber': ('django.db.models.fields.FloatField', [], {}),
            'half': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'test': ('django.db.models.fields.IntegerField', [], {}),
            'tto': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '30'})
        },
        'lab.pressure': {
            'Meta': {'object_name': 'Pressure'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'pressure_tests'", 'to': "orm['lab.Batch']"}),
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
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 19, 14, 8, 52, 3)'}),
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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 19, 0, 0)'}),
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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 19, 0, 0)'}),
            'delta': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.storedclay': {
            'Meta': {'object_name': 'StoredClay'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 19, 14, 8, 52, 3)'}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'lab.waterabsorption': {
            'Meta': {'object_name': 'WaterAbsorption'},
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 19, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['lab']