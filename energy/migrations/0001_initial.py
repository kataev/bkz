# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Energy'
        db.create_table('energy_energy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('elec4', self.gf('django.db.models.fields.FloatField')()),
            ('elec16', self.gf('django.db.models.fields.FloatField')()),
            ('iwater', self.gf('django.db.models.fields.FloatField')()),
            ('uwater', self.gf('django.db.models.fields.FloatField')()),
            ('gaz', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('energy', ['Energy'])

        # Adding model 'Teplo'
        db.create_table('energy_teplo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('henergy', self.gf('django.db.models.fields.FloatField')()),
            ('hot_water', self.gf('django.db.models.fields.FloatField')()),
            ('rpr', self.gf('django.db.models.fields.FloatField')()),
            ('robr', self.gf('django.db.models.fields.FloatField')()),
            ('tpr', self.gf('django.db.models.fields.FloatField')()),
            ('tobr', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('energy', ['Teplo'])

    def backwards(self, orm):
        # Deleting model 'Energy'
        db.delete_table('energy_energy')

        # Deleting model 'Teplo'
        db.delete_table('energy_teplo')

    models = {
        'energy.energy': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Energy'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'elec16': ('django.db.models.fields.FloatField', [], {}),
            'elec4': ('django.db.models.fields.FloatField', [], {}),
            'gaz': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iwater': ('django.db.models.fields.FloatField', [], {}),
            'uwater': ('django.db.models.fields.FloatField', [], {})
        },
        'energy.teplo': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Teplo'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'henergy': ('django.db.models.fields.FloatField', [], {}),
            'hot_water': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'robr': ('django.db.models.fields.FloatField', [], {}),
            'rpr': ('django.db.models.fields.FloatField', [], {}),
            'tobr': ('django.db.models.fields.FloatField', [], {}),
            'tpr': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['energy']