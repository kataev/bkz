# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Bill'
        db.create_table('sale_bill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 5, 3, 0, 0))),
            ('agent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sale_bill_related', to=orm['sale.Agent'])),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(default=350, related_name='proxy_sale_bill_related', to=orm['sale.Seller'])),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('sale', ['Bill'])

        # Adding model 'Sold'
        db.create_table('sale_sold', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brick_from', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='brick_from_solds', null=True, to=orm['brick.Brick'])),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(related_name='solds', to=orm['brick.Brick'])),
            ('tara', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('delivery', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('doc', self.gf('django.db.models.fields.related.ForeignKey')(related_name='solds', to=orm['sale.Bill'])),
        ))
        db.send_create_signal('sale', ['Sold'])

        # Adding model 'Pallet'
        db.create_table('sale_pallet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('poddon', self.gf('django.db.models.fields.PositiveIntegerField')(default=352)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('doc', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pallets', to=orm['sale.Bill'])),
        ))
        db.send_create_signal('sale', ['Pallet'])

        # Adding model 'Agent'
        db.create_table('sale_agent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('form', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('inn', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('kpp', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('bank', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('ks', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('bic', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('rs', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=600, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=600, blank=True)),
        ))
        db.send_create_signal('sale', ['Agent'])

        # Adding model 'OldAgent'
        db.create_table('sale_oldagent', (
            ('agent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sale.Agent'], unique=True, primary_key=True)),
            ('old', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('sale', ['OldAgent'])

        # Adding model 'Seller'
        db.create_table('sale_seller', (
            ('agent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sale.Agent'], unique=True, primary_key=True)),
            ('director', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('buhgalter', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('dispetcher', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('sale', ['Seller'])

        # Adding model 'Nomenclature'
        db.create_table('sale_nomenclature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=11)),
        ))
        db.send_create_signal('sale', ['Nomenclature'])

        # Adding model 'BuhAgent'
        db.create_table('sale_buhagent', (
            ('agent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sale.Agent'], unique=True, primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=11)),
        ))
        db.send_create_signal('sale', ['BuhAgent'])

    def backwards(self, orm):
        # Deleting model 'Bill'
        db.delete_table('sale_bill')

        # Deleting model 'Sold'
        db.delete_table('sale_sold')

        # Deleting model 'Pallet'
        db.delete_table('sale_pallet')

        # Deleting model 'Agent'
        db.delete_table('sale_agent')

        # Deleting model 'OldAgent'
        db.delete_table('sale_oldagent')

        # Deleting model 'Seller'
        db.delete_table('sale_seller')

        # Deleting model 'Nomenclature'
        db.delete_table('sale_nomenclature')

        # Deleting model 'BuhAgent'
        db.delete_table('sale_buhagent')

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
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sale_bill_related'", 'to': "orm['sale.Agent']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 5, 3, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'default': '350', 'related_name': "'proxy_sale_bill_related'", 'to': "orm['sale.Seller']"}),
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
            'director': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'dispetcher': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'sale.sold': {
            'Meta': {'ordering': "['-doc__date', '-doc__number']", 'object_name': 'Sold'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'solds'", 'to': "orm['brick.Brick']"}),
            'brick_from': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'brick_from_solds'", 'null': 'True', 'to': "orm['brick.Brick']"}),
            'delivery': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'solds'", 'to': "orm['sale.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'tara': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['sale']