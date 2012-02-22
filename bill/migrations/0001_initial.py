# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Bill'
        db.create_table('bill_bill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2012, 2, 22))),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('draft', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('agent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bill_bill_related', to=orm['agent.Agent'])),
            ('money', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('proxy', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='proxy_bill_bill_related', null=True, to=orm['agent.Agent'])),
        ))
        db.send_create_signal('bill', ['Bill'])

        # Adding model 'Transfer'
        db.create_table('bill_transfer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bill_transfer_related', to=orm['brick.Brick'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('tara', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('poddon', self.gf('django.db.models.fields.PositiveIntegerField')(default=352)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('doc', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='bill_transfer_related', null=True, to=orm['bill.Bill'])),
        ))
        db.send_create_signal('bill', ['Transfer'])

        # Adding model 'Sold'
        db.create_table('bill_sold', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bill_sold_related', to=orm['brick.Brick'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('tara', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('poddon', self.gf('django.db.models.fields.PositiveIntegerField')(default=352)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('delivery', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('doc', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='bill_sold_related', null=True, to=orm['bill.Bill'])),
        ))
        db.send_create_signal('bill', ['Sold'])

        # Adding M2M table for field transfer on 'Sold'
        db.create_table('bill_sold_transfer', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sold', models.ForeignKey(orm['bill.sold'], null=False)),
            ('transfer', models.ForeignKey(orm['bill.transfer'], null=False))
        ))
        db.create_unique('bill_sold_transfer', ['sold_id', 'transfer_id'])


    def backwards(self, orm):
        
        # Deleting model 'Bill'
        db.delete_table('bill_bill')

        # Deleting model 'Transfer'
        db.delete_table('bill_transfer')

        # Deleting model 'Sold'
        db.delete_table('bill_sold')

        # Removing M2M table for field transfer on 'Sold'
        db.delete_table('bill_sold_transfer')


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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2012, 2, 22)'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'money': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'proxy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'proxy_bill_bill_related'", 'null': 'True', 'to': "orm['agent.Agent']"})
        },
        'bill.sold': {
            'Meta': {'object_name': 'Sold'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bill_sold_related'", 'to': "orm['brick.Brick']"}),
            'delivery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'bill_sold_related'", 'null': 'True', 'to': "orm['bill.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'poddon': ('django.db.models.fields.PositiveIntegerField', [], {'default': '352'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'tara': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'transfer': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'bill_sold_related'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['bill.Transfer']"})
        },
        'bill.transfer': {
            'Meta': {'object_name': 'Transfer'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bill_transfer_related'", 'to': "orm['brick.Brick']"}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'bill_transfer_related'", 'null': 'True', 'to': "orm['bill.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'poddon': ('django.db.models.fields.PositiveIntegerField', [], {'default': '352'}),
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
