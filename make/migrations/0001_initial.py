# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Forming'
        db.create_table('make_forming', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 8, 0, 0))),
            ('cavitation', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('width', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['whs.Width'])),
            ('color', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('tts', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('make', ['Forming'])

        # Adding model 'Warren'
        db.create_table('make_warren', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 8, 0, 0), null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='consumer', null=True, to=orm['make.Warren'])),
            ('amount', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('make', ['Warren'])

    def backwards(self, orm):
        # Deleting model 'Forming'
        db.delete_table('make_forming')

        # Deleting model 'Warren'
        db.delete_table('make_warren')

    models = {
        'make.forming': {
            'Meta': {'object_name': 'Forming'},
            'cavitation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 8, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tts': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'width': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['whs.Width']"})
        },
        'make.warren': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Warren'},
            'amount': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 8, 0, 0)', 'null': 'True', 'blank': 'True'}),
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