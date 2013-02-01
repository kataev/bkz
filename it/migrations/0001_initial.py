# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Device'
        db.create_table('it_device', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['it.Device'], null=True, blank=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=600, blank=True)),
        ))
        db.send_create_signal('it', ['Device'])

        # Adding M2M table for field allowed on 'Device'
        db.create_table('it_device_allowed', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_device', models.ForeignKey(orm['it.device'], null=False)),
            ('to_device', models.ForeignKey(orm['it.device'], null=False))
        ))
        db.create_unique('it_device_allowed', ['from_device_id', 'to_device_id'])

        # Adding model 'Buy'
        db.create_table('it_buy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cartridge', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'buy', to=orm['it.Device'])),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 2, 1, 0, 0))),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=600, blank=True)),
        ))
        db.send_create_signal('it', ['Buy'])

        # Adding model 'Plug'
        db.create_table('it_plug', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'plug', to=orm['it.Buy'])),
            ('printer', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'plug', to=orm['it.Device'])),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 2, 1, 0, 0))),
        ))
        db.send_create_signal('it', ['Plug'])

    def backwards(self, orm):
        # Deleting model 'Device'
        db.delete_table('it_device')

        # Removing M2M table for field allowed on 'Device'
        db.delete_table('it_device_allowed')

        # Deleting model 'Buy'
        db.delete_table('it_buy')

        # Deleting model 'Plug'
        db.delete_table('it_plug')

    models = {
        'it.buy': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Buy'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cartridge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'buy'", 'to': "orm['it.Device']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 2, 1, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '600', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {})
        },
        'it.device': {
            'Meta': {'ordering': "('type__name', 'place', 'name')", 'object_name': 'Device'},
            'allowed': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'allowed_rel_+'", 'null': 'True', 'to': "orm['it.Device']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '600', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['it.Device']", 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'it.plug': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Plug'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'plug'", 'to': "orm['it.Buy']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 2, 1, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'printer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'plug'", 'to': "orm['it.Device']"})
        }
    }

    complete_apps = ['it']