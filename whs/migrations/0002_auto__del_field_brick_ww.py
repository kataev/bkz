# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Brick.ww'
        db.delete_column('whs_brick', 'ww')

    def backwards(self, orm):
        # Adding field 'Brick.ww'
        db.add_column('whs_brick', 'ww',
                      self.gf('django.db.models.fields.FloatField')(default=1.4),
                      keep_default=False)

    models = {
        'whs.agent': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Agent'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'bank': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'bic': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'form': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '600', 'blank': 'True'}),
            'inn': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'kpp': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'ks': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400', 'db_index': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'rs': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '600', 'blank': 'True'})
        },
        'whs.bill': {
            'Meta': {'ordering': "['-date', '-number']", 'object_name': 'Bill'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "u'bill_agents'", 'to': "orm['whs.Agent']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 15, 0, 0)', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'default': '350', 'related_name': "'bill_sallers'", 'to': "orm['whs.Seller']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'})
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
            'width': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['whs.Width']"})
        },
        'whs.buhagent': {
            'Meta': {'object_name': 'BuhAgent'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buhagent'", 'to': "orm['whs.Agent']"}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'whs.features': {
            'Meta': {'ordering': "('type',)", 'object_name': 'Features'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'whs.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 15, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'})
        },
        'whs.nomenclature': {
            'Meta': {'object_name': 'Nomenclature'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'whs.oldagent': {
            'Meta': {'object_name': 'OldAgent'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'oldagent'", 'to': "orm['whs.Agent']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old': ('django.db.models.fields.IntegerField', [], {})
        },
        'whs.oldbrick': {
            'Meta': {'object_name': 'OldBrick'},
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'oldbrick'", 'to': "orm['whs.Brick']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old': ('django.db.models.fields.IntegerField', [], {}),
            'prim': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '260'})
        },
        'whs.pallet': {
            'Meta': {'object_name': 'Pallet'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pallets'", 'to': "orm['whs.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'poddon': ('django.db.models.fields.PositiveIntegerField', [], {'default': '352'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': '200'})
        },
        'whs.seller': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Seller', '_ormbases': ['whs.Agent']},
            'agent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['whs.Agent']", 'unique': 'True', 'primary_key': 'True'}),
            'buhgalter': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'director': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'dispetcher': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nds': ('django.db.models.fields.FloatField', [], {'default': '0.18'})
        },
        'whs.sold': {
            'Meta': {'ordering': "['-doc__date', '-doc__number']", 'object_name': 'Sold'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'batch_number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'batch_year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2013', 'null': 'True', 'blank': 'True'}),
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sold_brick'", 'to': "orm['whs.Brick']"}),
            'brick_from': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sold_brick_from'", 'null': 'True', 'to': "orm['whs.Brick']"}),
            'delivery': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'solds'", 'to': "orm['whs.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'tara': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'whs.sorting': {
            'Meta': {'object_name': 'Sorting'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'batch_number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'batch_year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2013', 'null': 'True', 'blank': 'True'}),
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sorting'", 'to': "orm['whs.Brick']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 15, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sorted'", 'null': 'True', 'to': "orm['whs.Sorting']"}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'whs.width': {
            'Meta': {'ordering': "('pk',)", 'object_name': 'Width'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'type': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'whs.write_off': {
            'Meta': {'object_name': 'Write_off'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'write_off'", 'to': "orm['whs.Brick']"}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'write_off'", 'to': "orm['whs.Inventory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['whs']