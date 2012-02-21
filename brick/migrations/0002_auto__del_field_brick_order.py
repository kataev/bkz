# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Brick.order'
        db.delete_column('brick_brick', 'order')


    def backwards(self, orm):
        
        # Adding field 'Brick.order'
        db.add_column('brick_brick', 'order', self.gf('django.db.models.fields.IntegerField')(default=1000, db_index=True), keep_default=False)


    models = {
        'brick.brick': {
            'Meta': {'ordering': "('-weight', 'color', '-view', 'ctype', 'defect', 'features', 'refuse', 'mark', 'id')", 'object_name': 'Brick'},
            'color': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'css': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '360'}),
            'ctype': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '6', 'blank': 'True'}),
            'defect': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '60', 'blank': 'True'}),
            'features': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '660'}),
            'mark': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '160'}),
            'refuse': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '10'}),
            'total': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'view': ('django.db.models.fields.CharField', [], {'default': "u'\\u041b'", 'max_length': '60'}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '1.4'})
        },
        'brick.history': {
            'Meta': {'object_name': 'History'},
            'add': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'begin': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'brick_history_related'", 'to': "orm['brick.Brick']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sold': ('django.db.models.fields.PositiveIntegerField', [], {}),
            't_from': ('django.db.models.fields.PositiveIntegerField', [], {}),
            't_to': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'total': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['brick']
