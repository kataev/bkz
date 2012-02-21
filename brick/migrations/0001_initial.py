# encoding: utf-8
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
            ('refuse', self.gf('django.db.models.fields.CharField')(default=u'', max_length=10)),
            ('features', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=160)),
            ('css', self.gf('django.db.models.fields.CharField')(default=u'', max_length=360)),
            ('label', self.gf('django.db.models.fields.CharField')(default='', max_length=660)),
            ('total', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=1000, db_index=True)),
        ))
        db.send_create_signal('brick', ['Brick'])

        # Adding model 'History'
        db.create_table('brick_history', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(related_name='brick_history_related', to=orm['brick.Brick'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('begin', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('add', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('t_from', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('t_to', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('sold', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('total', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('brick', ['History'])


    def backwards(self, orm):
        
        # Deleting model 'Brick'
        db.delete_table('brick_brick')

        # Deleting model 'History'
        db.delete_table('brick_history')


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
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1000', 'db_index': 'True'}),
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
