# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Man'
        db.create_table('man_man', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 5, 15, 0, 0), unique=True)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('man', ['Man'])

        # Adding model 'Add'
        db.create_table('man_add', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(related_name='man_add_related', to=orm['brick.Brick'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('doc', self.gf('django.db.models.fields.related.ForeignKey')(related_name='man_add_related', to=orm['man.Man'])),
        ))
        db.send_create_signal('man', ['Add'])

        # Adding model 'Sorting'
        db.create_table('man_sorting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 5, 15, 0, 0))),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(related_name='man_sorting_related', to=orm['brick.Brick'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('man', ['Sorting'])

        # Adding model 'Sorted'
        db.create_table('man_sorted', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(related_name='man_sorted_related', to=orm['brick.Brick'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 5, 15, 0, 0), unique=True)),
            ('doc', self.gf('django.db.models.fields.related.ForeignKey')(related_name='man_sorted_related', to=orm['man.Sorting'])),
        ))
        db.send_create_signal('man', ['Sorted'])

        # Adding model 'Removed'
        db.create_table('man_removed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(related_name='man_removed_related', to=orm['brick.Brick'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 5, 15, 0, 0), unique=True)),
            ('doc', self.gf('django.db.models.fields.related.ForeignKey')(related_name='man_removed_related', to=orm['man.Sorting'])),
        ))
        db.send_create_signal('man', ['Removed'])

        # Adding model 'Inventory'
        db.create_table('man_inventory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 5, 15, 0, 0))),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('man', ['Inventory'])

        # Adding model 'Write_off'
        db.create_table('man_write_off', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(related_name='man_write_off_related', to=orm['brick.Brick'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('doc', self.gf('django.db.models.fields.related.ForeignKey')(related_name='man_write_off_related', to=orm['man.Inventory'])),
        ))
        db.send_create_signal('man', ['Write_off'])

    def backwards(self, orm):
        # Deleting model 'Man'
        db.delete_table('man_man')

        # Deleting model 'Add'
        db.delete_table('man_add')

        # Deleting model 'Sorting'
        db.delete_table('man_sorting')

        # Deleting model 'Sorted'
        db.delete_table('man_sorted')

        # Deleting model 'Removed'
        db.delete_table('man_removed')

        # Deleting model 'Inventory'
        db.delete_table('man_inventory')

        # Deleting model 'Write_off'
        db.delete_table('man_write_off')

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
        'man.add': {
            'Meta': {'ordering': "('-doc__date',)", 'object_name': 'Add'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'man_add_related'", 'to': "orm['brick.Brick']"}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'man_add_related'", 'to': "orm['man.Man']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'man.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 5, 15, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'})
        },
        'man.man': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Man'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 5, 15, 0, 0)', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'})
        },
        'man.removed': {
            'Meta': {'object_name': 'Removed'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'man_removed_related'", 'to': "orm['brick.Brick']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 5, 15, 0, 0)', 'unique': 'True'}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'man_removed_related'", 'to': "orm['man.Sorting']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'man.sorted': {
            'Meta': {'object_name': 'Sorted'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'man_sorted_related'", 'to': "orm['brick.Brick']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 5, 15, 0, 0)', 'unique': 'True'}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'man_sorted_related'", 'to': "orm['man.Sorting']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'man.sorting': {
            'Meta': {'object_name': 'Sorting'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'man_sorting_related'", 'to': "orm['brick.Brick']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 5, 15, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'man.write_off': {
            'Meta': {'object_name': 'Write_off'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'man_write_off_related'", 'to': "orm['brick.Brick']"}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'man_write_off_related'", 'to': "orm['man.Inventory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sale.nomenclature': {
            'Meta': {'object_name': 'Nomenclature'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['man']