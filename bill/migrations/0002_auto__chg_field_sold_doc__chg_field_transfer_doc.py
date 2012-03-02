# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Sold.doc'
        db.alter_column('bill_sold', 'doc_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['bill.Bill']))

        # Changing field 'Transfer.doc'
        db.alter_column('bill_transfer', 'doc_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['bill.Bill']))


    def backwards(self, orm):
        
        # Changing field 'Sold.doc'
        db.alter_column('bill_sold', 'doc_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['bill.Bill']))

        # Changing field 'Transfer.doc'
        db.alter_column('bill_transfer', 'doc_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['bill.Bill']))


    models = {
        'agent.agent': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Agent'},
            'account': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'bank': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'form': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inn': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'bill.bill': {
            'Meta': {'ordering': "['-date', '-number']", 'object_name': 'Bill'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bill_bill_related'", 'to': "orm['agent.Agent']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2012, 3, 1)'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proxy_bill_bill_related'", 'to': "orm['agent.Agent']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'})
        },
        'bill.sold': {
            'Meta': {'object_name': 'Sold'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bill_sold_related'", 'to': "orm['brick.Brick']"}),
            'delivery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bill_sold_related'", 'to': "orm['bill.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'poddon': ('django.db.models.fields.PositiveIntegerField', [], {'default': '352'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'tara': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'bill.transfer': {
            'Meta': {'object_name': 'Transfer'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'brick_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'brick_from_bill_transfer_related'", 'to': "orm['brick.Brick']"}),
            'brick_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'brick_to_bill_transfer_related'", 'to': "orm['brick.Brick']"}),
            'delivery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bill_transfer_related'", 'to': "orm['bill.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'poddon': ('django.db.models.fields.PositiveIntegerField', [], {'default': '352'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'tara': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
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
        }
    }

    complete_apps = ['bill']
