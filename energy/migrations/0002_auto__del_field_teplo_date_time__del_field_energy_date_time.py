# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Teplo.date_time'
        db.delete_column('energy_teplo', 'date_time')

        # Deleting field 'Energy.date_time'
        db.delete_column('energy_energy', 'date_time')

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Teplo.date_time'
        raise RuntimeError("Cannot reverse this migration. 'Teplo.date_time' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Energy.date_time'
        raise RuntimeError("Cannot reverse this migration. 'Energy.date_time' and its values cannot be restored.")
    models = {
        'energy.energy': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Energy'},
            'date': ('django.db.models.fields.DateField', [], {}),
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