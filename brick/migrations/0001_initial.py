# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Brick'
        db.create_table('brick_brick', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('color', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('mark', self.gf('django.db.models.fields.PositiveIntegerField')(default=100)),
            ('weight', self.gf('django.db.models.fields.FloatField')(default=1.4)),
            ('view', self.gf('django.db.models.fields.CharField')(default=u'\u041b', max_length=60)),
            ('ctype', self.gf('django.db.models.fields.CharField')(default='', max_length=6, blank=True)),
            ('defect', self.gf('django.db.models.fields.CharField')(default=u'', max_length=60, blank=True)),
            ('refuse', self.gf('django.db.models.fields.CharField')(default=u'', max_length=10, blank=True)),
            ('features', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=160)),
            ('css', self.gf('django.db.models.fields.CharField')(default=u'', max_length=360)),
            ('label', self.gf('django.db.models.fields.CharField')(default='', max_length=660)),
            ('total', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('nomenclature', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sale.Nomenclature'], null=True, blank=True)),
        ))
        db.send_create_signal('brick', ['Brick'])

        # Adding model 'OldBrick'
        db.create_table('brick_oldbrick', (
            ('brick_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['brick.Brick'], unique=True, primary_key=True)),
            ('old', self.gf('django.db.models.fields.IntegerField')()),
            ('prim', self.gf('django.db.models.fields.CharField')(default='', max_length=260)),
        ))
        db.send_create_signal('brick', ['OldBrick'])

    def backwards(self, orm):
        # Deleting model 'Brick'
        db.delete_table('brick_brick')

        # Deleting model 'OldBrick'
        db.delete_table('brick_oldbrick')

    models = {
        'brick.brick': {
            'Meta': {'ordering': "('-weight', 'color', '-view', 'ctype', 'defect', 'features', 'mark', 'refuse', 'id')", 'object_name': 'Brick'},
            'color': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'css': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '360'}),
            'ctype': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '6', 'blank': 'True'}),
            'defect': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '60', 'blank': 'True'}),
            'features': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '660'}),
            'mark': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '160'}),
            'nomenclature': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sale.Nomenclature']", 'null': 'True', 'blank': 'True'}),
            'refuse': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '10', 'blank': 'True'}),
            'total': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'view': ('django.db.models.fields.CharField', [], {'default': "u'\\u041b'", 'max_length': '60'}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '1.4'})
        },
        'brick.oldbrick': {
            'Meta': {'ordering': "('-weight', 'color', '-view', 'ctype', 'defect', 'features', 'mark', 'refuse', 'id')", 'object_name': 'OldBrick', '_ormbases': ['brick.Brick']},
            'brick_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['brick.Brick']", 'unique': 'True', 'primary_key': 'True'}),
            'old': ('django.db.models.fields.IntegerField', [], {}),
            'prim': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '260'})
        },
        'sale.nomenclature': {
            'Meta': {'object_name': 'Nomenclature'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['brick']