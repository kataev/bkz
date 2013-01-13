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
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 6, 0, 0))),
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
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 6, 0, 0))),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('humidity', self.gf('django.db.models.fields.FloatField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['StoredClay'])

        # Adding model 'Sand'
        db.create_table('lab_sand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 6, 0, 0))),
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
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 6, 0, 0))),
            ('cavitation', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('color', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('width', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['whs.Width'])),
            ('tts', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('temperature', self.gf('django.db.models.fields.FloatField')()),
            ('weight', self.gf('django.db.models.fields.FloatField')()),
            ('humidity', self.gf('django.db.models.fields.FloatField')()),
            ('sand', self.gf('django.db.models.fields.FloatField')()),
            ('humidity_transporter', self.gf('django.db.models.fields.FloatField')()),
            ('poke_left', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=300)),
            ('poke_right', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=300)),
            ('stratcher_left', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=300)),
            ('stratcher_right', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=300)),
            ('cutter', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=3000)),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000)),
        ))
        db.send_create_signal('lab', ['Bar'])

        # Adding model 'Raw'
        db.create_table('lab_raw', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 6, 0, 0))),
            ('cavitation', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('color', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('width', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['whs.Width'])),
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
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 6, 0, 0))),
            ('cavitation', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('color', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('width', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['whs.Width'])),
            ('path', self.gf('django.db.models.fields.IntegerField')()),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('tts', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('humidity', self.gf('django.db.models.fields.FloatField')()),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('weight', self.gf('django.db.models.fields.FloatField')()),
            ('shrink', self.gf('django.db.models.fields.FloatField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['Half'])

        # Adding model 'WaterAbsorption'
        db.create_table('lab_waterabsorption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 6, 0, 0))),
            ('width', self.gf('django.db.models.fields.FloatField')(default=0.8, max_length=30)),
            ('color', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['WaterAbsorption'])

        # Adding model 'Efflorescence'
        db.create_table('lab_efflorescence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 6, 0, 0))),
            ('color', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['Efflorescence'])

        # Adding model 'FrostResistance'
        db.create_table('lab_frostresistance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 6, 0, 0))),
            ('width', self.gf('django.db.models.fields.FloatField')(default=0.8, max_length=30)),
            ('mark', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('color', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['FrostResistance'])

        # Adding model 'SEONR'
        db.create_table('lab_seonr', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 6, 0, 0))),
            ('color', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('delta', self.gf('django.db.models.fields.FloatField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['SEONR'])

        # Adding model 'HeatConduction'
        db.create_table('lab_heatconduction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 6, 0, 0))),
            ('width', self.gf('django.db.models.fields.FloatField')(default=0.8, max_length=30)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['HeatConduction'])

        # Adding model 'Batch'
        db.create_table('lab_batch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 6, 0, 0))),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cavitation', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('view', self.gf('django.db.models.fields.CharField')(default=u'\u041b', max_length=60)),
            ('color', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ctype', self.gf('django.db.models.fields.CharField')(default='0', max_length=6)),
            ('width', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['whs.Width'])),
            ('heatconduction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab.HeatConduction'], null=True, blank=True)),
            ('seonr', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab.SEONR'], null=True, blank=True)),
            ('frost_resistance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab.FrostResistance'], null=True, blank=True)),
            ('water_absorption', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab.WaterAbsorption'], null=True, blank=True)),
            ('volume', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='volume_test', null=True, to=orm['lab.Test'])),
            ('cad', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('density', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('weight', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('tto', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('pressure', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('flexion', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mark', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('chamfer', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('pf', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=300, null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['Batch'])

        # Adding model 'Cause'
        db.create_table('lab_cause', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('lab', ['Cause'])

        # Adding model 'Part'
        db.create_table('lab_part', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parts', to=orm['lab.Batch'])),
            ('defect', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('dnumber', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('half', self.gf('django.db.models.fields.FloatField')(default=3.0)),
            ('limestone', self.gf('bkz.lab.models.RangeField')(max_length=30, null=True, blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['whs.Brick'], null=True, blank=True)),
        ))
        db.send_create_signal('lab', ['Part'])

        # Adding M2M table for field cause on 'Part'
        db.create_table('lab_part_cause', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('part', models.ForeignKey(orm['lab.part'], null=False)),
            ('cause', models.ForeignKey(orm['lab.cause'], null=False))
        ))
        db.create_unique('lab_part_cause', ['part_id', 'cause_id'])

        # Adding model 'RowPart'
        db.create_table('lab_rowpart', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('part', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rows', to=orm['lab.Part'])),
            ('tto', self.gf('bkz.lab.models.RangeField')(max_length=30)),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
            ('test', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('brocken', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('lab', ['RowPart'])

        # Adding model 'Test'
        db.create_table('lab_test', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'tests', to=orm['lab.Batch'])),
            ('tto', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('row', self.gf('django.db.models.fields.IntegerField')()),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('area', self.gf('django.db.models.fields.FloatField')()),
            ('readings', self.gf('django.db.models.fields.FloatField')()),
            ('value', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal('lab', ['Test'])

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

        # Deleting model 'SEONR'
        db.delete_table('lab_seonr')

        # Deleting model 'HeatConduction'
        db.delete_table('lab_heatconduction')

        # Deleting model 'Batch'
        db.delete_table('lab_batch')

        # Deleting model 'Cause'
        db.delete_table('lab_cause')

        # Deleting model 'Part'
        db.delete_table('lab_part')

        # Removing M2M table for field cause on 'Part'
        db.delete_table('lab_part_cause')

        # Deleting model 'RowPart'
        db.delete_table('lab_rowpart')

        # Deleting model 'Test'
        db.delete_table('lab_test')

    models = {
        'lab.bar': {
            'Meta': {'ordering': "('-datetime',)", 'object_name': 'Bar'},
            'cavitation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cutter': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '3000'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 6, 0, 0)'}),
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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 6, 0, 0)'}),
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
            'Meta': {'ordering': "('-datetime',)", 'object_name': 'Clay'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 6, 0, 0)'}),
            'dust': ('django.db.models.fields.FloatField', [], {}),
            'humidity': ('bkz.lab.models.SlashSeparatedFloatField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusion': ('django.db.models.fields.FloatField', [], {}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'sand': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.efflorescence': {
            'Meta': {'object_name': 'Efflorescence'},
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 6, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'})
        },
        'lab.frostresistance': {
            'Meta': {'object_name': 'FrostResistance'},
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 6, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'mark': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'value': ('django.db.models.fields.IntegerField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {'default': '0.8', 'max_length': '30'})
        },
        'lab.half': {
            'Meta': {'ordering': "('-datetime', '-path', '-position')", 'object_name': 'Half'},
            'cavitation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 6, 0, 0)'}),
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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 6, 0, 0)'}),
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
            'Meta': {'ordering': "('-datetime',)", 'object_name': 'Raw'},
            'cavitation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 6, 0, 0)'}),
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
            'Meta': {'ordering': "('-datetime',)", 'object_name': 'Sand'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 6, 0, 0)'}),
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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 6, 0, 0)'}),
            'delta': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.storedclay': {
            'Meta': {'ordering': "('-datetime', '-position')", 'object_name': 'StoredClay'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 6, 0, 0)'}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '1'})
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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 6, 0, 0)'}),
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