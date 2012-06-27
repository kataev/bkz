# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Seller.director_name'
        db.add_column('sale_seller', 'director_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Seller.buhgalter_name'
        db.add_column('sale_seller', 'buhgalter_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Seller.dispetcher_name'
        db.add_column('sale_seller', 'dispetcher_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Seller.director_name'
        db.delete_column('sale_seller', 'director_name')

        # Deleting field 'Seller.buhgalter_name'
        db.delete_column('sale_seller', 'buhgalter_name')

        # Deleting field 'Seller.dispetcher_name'
        db.delete_column('sale_seller', 'dispetcher_name')

    models = {
        'brick.brick': {
            'Meta': {'ordering': "('-weight', 'color', '-view', 'ctype', 'defect', 'features', 'mark', 'refuse', 'id')", 'object_name': 'Brick'},
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
            'weight': ('django.db.models.fields.FloatField', [], {'default': '1.4'})
        },
        'sale.agent': {
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'rs': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '600', 'blank': 'True'})
        },
        'sale.bill': {
            'Meta': {'ordering': "['-date', '-number']", 'object_name': 'Bill'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'bill_agents'", 'to': "orm['sale.Agent']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 5, 10, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'default': '350', 'related_name': "'bill_sallers'", 'to': "orm['sale.Seller']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'})
        },
        'sale.buhagent': {
            'Meta': {'ordering': "('name',)", 'object_name': 'BuhAgent', '_ormbases': ['sale.Agent']},
            'agent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sale.Agent']", 'unique': 'True', 'primary_key': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'})
        },
        'sale.nomenclature': {
            'Meta': {'object_name': 'Nomenclature'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'sale.oldagent': {
            'Meta': {'ordering': "('name',)", 'object_name': 'OldAgent', '_ormbases': ['sale.Agent']},
            'agent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sale.Agent']", 'unique': 'True', 'primary_key': 'True'}),
            'old': ('django.db.models.fields.IntegerField', [], {})
        },
        'sale.pallet': {
            'Meta': {'object_name': 'Pallet'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pallets'", 'to': "orm['sale.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'poddon': ('django.db.models.fields.PositiveIntegerField', [], {'default': '352'})
        },
        'sale.seller': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Seller', '_ormbases': ['sale.Agent']},
            'agent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sale.Agent']", 'unique': 'True', 'primary_key': 'True'}),
            'buhgalter': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'buhgalter_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'director': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'director_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'dispetcher': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'dispetcher_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nds': ('django.db.models.fields.FloatField', [], {'default': '0.18'})
        },
        'sale.sold': {
            'Meta': {'ordering': "['-doc__date', '-doc__number']", 'object_name': 'Sold'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sold_brick'", 'to': "orm['brick.Brick']"}),
            'brick_from': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sold_brick_from'", 'null': 'True', 'to': "orm['brick.Brick']"}),
            'delivery': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'solds'", 'to': "orm['sale.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'tara': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['sale']