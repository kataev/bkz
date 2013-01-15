# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Width'
        db.create_table('whs_width', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('type', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('whs', ['Width'])

        # Adding model 'Features'
        db.create_table('whs_features', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('whs', ['Features'])

        # Adding model 'Brick'
        db.create_table('whs_brick', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cavitation', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('color', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('mark', self.gf('django.db.models.fields.PositiveIntegerField')(default=100)),
            ('width', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['whs.Width'])),
            ('ww', self.gf('django.db.models.fields.FloatField')(default=1.4)),
            ('view', self.gf('django.db.models.fields.CharField')(default=u'\u041b', max_length=60)),
            ('ctype', self.gf('django.db.models.fields.CharField')(default='0', max_length=6, blank=True)),
            ('defect', self.gf('django.db.models.fields.CharField')(default=u'gost', max_length=60, blank=True)),
            ('refuse', self.gf('django.db.models.fields.CharField')(default=u'', max_length=10, blank=True)),
            ('frost_resistance', self.gf('django.db.models.fields.PositiveIntegerField')(default=50)),
            ('cad', self.gf('django.db.models.fields.FloatField')()),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=160)),
            ('css', self.gf('django.db.models.fields.CharField')(default=u'', max_length=360)),
            ('label', self.gf('django.db.models.fields.CharField')(default='', max_length=660)),
            ('total', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('mass', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('nomenclature', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['whs.Nomenclature'], null=True, blank=True)),
        ))
        db.send_create_signal('whs', ['Brick'])

        # Adding M2M table for field features on 'Brick'
        db.create_table('whs_brick_features', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('brick', models.ForeignKey(orm['whs.brick'], null=False)),
            ('features', models.ForeignKey(orm['whs.features'], null=False))
        ))
        db.create_unique('whs_brick_features', ['brick_id', 'features_id'])

        # Adding model 'OldBrick'
        db.create_table('whs_oldbrick', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(related_name='oldbrick', to=orm['whs.Brick'])),
            ('old', self.gf('django.db.models.fields.IntegerField')()),
            ('prim', self.gf('django.db.models.fields.CharField')(default='', max_length=260)),
        ))
        db.send_create_signal('whs', ['OldBrick'])

        # Adding model 'Agent'
        db.create_table('whs_agent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=400, db_index=True)),
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
        db.send_create_signal('whs', ['Agent'])

        # Adding model 'Seller'
        db.create_table('whs_seller', (
            ('agent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['whs.Agent'], unique=True, primary_key=True)),
            ('director', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('buhgalter', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('dispetcher', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('nds', self.gf('django.db.models.fields.FloatField')(default=0.18)),
        ))
        db.send_create_signal('whs', ['Seller'])

        # Adding model 'OldAgent'
        db.create_table('whs_oldagent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='oldagent', to=orm['whs.Agent'])),
            ('old', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('whs', ['OldAgent'])

        # Adding model 'Bill'
        db.create_table('whs_bill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 8, 0, 0), db_index=True)),
            ('agent', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name=u'bill_agents', to=orm['whs.Agent'])),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(default=350, related_name='bill_sallers', to=orm['whs.Seller'])),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('whs', ['Bill'])

        # Adding model 'Pallet'
        db.create_table('whs_pallet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('poddon', self.gf('django.db.models.fields.PositiveIntegerField')(default=352)),
            ('price', self.gf('django.db.models.fields.FloatField')(default=200)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('doc', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pallets', to=orm['whs.Bill'])),
        ))
        db.send_create_signal('whs', ['Pallet'])

        # Adding model 'Sold'
        db.create_table('whs_sold', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brick_from', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sold_brick_from', null=True, to=orm['whs.Brick'])),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sold_brick', to=orm['whs.Brick'])),
            ('batch_number', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('batch_year', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2013, null=True, blank=True)),
            ('tara', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('price', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('delivery', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('doc', self.gf('django.db.models.fields.related.ForeignKey')(related_name='solds', to=orm['whs.Bill'])),
        ))
        db.send_create_signal('whs', ['Sold'])

        # Adding model 'Nomenclature'
        db.create_table('whs_nomenclature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=11)),
        ))
        db.send_create_signal('whs', ['Nomenclature'])

        # Adding model 'BuhAgent'
        db.create_table('whs_buhagent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='buhagent', to=orm['whs.Agent'])),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=11)),
        ))
        db.send_create_signal('whs', ['BuhAgent'])

        # Adding model 'Sorting'
        db.create_table('whs_sorting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 8, 0, 0))),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sorting', to=orm['whs.Brick'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('batch_number', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('batch_year', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2013, null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sorted', null=True, to=orm['whs.Sorting'])),
        ))
        db.send_create_signal('whs', ['Sorting'])

        # Adding model 'Inventory'
        db.create_table('whs_inventory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 8, 0, 0))),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('whs', ['Inventory'])

        # Adding model 'Write_off'
        db.create_table('whs_write_off', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(related_name='write_off', to=orm['whs.Brick'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('doc', self.gf('django.db.models.fields.related.ForeignKey')(related_name='write_off', to=orm['whs.Inventory'])),
        ))
        db.send_create_signal('whs', ['Write_off'])

    def backwards(self, orm):
        # Deleting model 'Width'
        db.delete_table('whs_width')

        # Deleting model 'Features'
        db.delete_table('whs_features')

        # Deleting model 'Brick'
        db.delete_table('whs_brick')

        # Removing M2M table for field features on 'Brick'
        db.delete_table('whs_brick_features')

        # Deleting model 'OldBrick'
        db.delete_table('whs_oldbrick')

        # Deleting model 'Agent'
        db.delete_table('whs_agent')

        # Deleting model 'Seller'
        db.delete_table('whs_seller')

        # Deleting model 'OldAgent'
        db.delete_table('whs_oldagent')

        # Deleting model 'Bill'
        db.delete_table('whs_bill')

        # Deleting model 'Pallet'
        db.delete_table('whs_pallet')

        # Deleting model 'Sold'
        db.delete_table('whs_sold')

        # Deleting model 'Nomenclature'
        db.delete_table('whs_nomenclature')

        # Deleting model 'BuhAgent'
        db.delete_table('whs_buhagent')

        # Deleting model 'Sorting'
        db.delete_table('whs_sorting')

        # Deleting model 'Inventory'
        db.delete_table('whs_inventory')

        # Deleting model 'Write_off'
        db.delete_table('whs_write_off')

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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 8, 0, 0)', 'db_index': 'True'}),
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
            'width': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['whs.Width']"}),
            'ww': ('django.db.models.fields.FloatField', [], {'default': '1.4'})
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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 8, 0, 0)'}),
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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 8, 0, 0)'}),
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