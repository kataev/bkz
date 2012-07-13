# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Batch'
        db.delete_table('brick_batch')

    def backwards(self, orm):
        # Adding model 'Batch'
        db.create_table('brick_batch', (
            ('info', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('brick_lab', self.gf('django.db.models.fields.related.ForeignKey')(related_name='batch_lab', to=orm['brick.Brick'])),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 7, 6, 0, 0))),
            ('brick_whs', self.gf('django.db.models.fields.related.ForeignKey')(related_name='batch_whs', to=orm['brick.Brick'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('brick', ['Batch'])

    models = {
        'brick.brick': {
            'Meta': {'ordering': "('-width', 'color', '-view', 'ctype', 'defect', 'features', 'mark', 'refuse', 'id')", 'object_name': 'Brick'},
            'cavitation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
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
            'width': ('django.db.models.fields.FloatField', [], {'default': '1.4'})
        },
        'brick.oldbrick': {
            'Meta': {'ordering': "('-width', 'color', '-view', 'ctype', 'defect', 'features', 'mark', 'refuse', 'id')", 'object_name': 'OldBrick', '_ormbases': ['brick.Brick']},
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