# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Add'
        db.create_table('whs_add', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('part', self.gf('django.db.models.fields.related.ForeignKey')(related_name='add', to=orm['lab.Part'])),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(related_name='man', to=orm['whs.Brick'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('doc', self.gf('django.db.models.fields.related.ForeignKey')(related_name='add', to=orm['whs.Man'])),
        ))
        db.send_create_signal('whs', ['Add'])

        # Adding model 'Write_off'
        db.create_table('whs_write_off', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(related_name='write_off', to=orm['whs.Brick'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('doc', self.gf('django.db.models.fields.related.ForeignKey')(related_name='write_off', to=orm['whs.Inventory'])),
        ))
        db.send_create_signal('whs', ['Write_off'])

        # Adding model 'Price'
        db.create_table('whs_price', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['whs.Brick'])),
            ('price', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('whs', ['Price'])

        # Adding model 'Sorting'
        db.create_table('whs_sorting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 7, 18, 0, 0))),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sorting', to=orm['lab.Batch'])),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sorting', to=orm['whs.Brick'])),
            ('brick_from', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sorting_from', to=orm['whs.Brick'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('whs', ['Sorting'])

        # Adding model 'Agent'
        db.create_table('whs_agent', (
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
        db.send_create_signal('whs', ['Agent'])

        # Adding model 'OldAgent'
        db.create_table('whs_oldagent', (
            ('agent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['whs.Agent'], unique=True, primary_key=True)),
            ('old', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('whs', ['OldAgent'])

        # Adding model 'Pallet'
        db.create_table('whs_pallet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('poddon', self.gf('django.db.models.fields.PositiveIntegerField')(default=352)),
            ('price', self.gf('django.db.models.fields.FloatField')(default=200)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('doc', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pallets', to=orm['whs.Bill'])),
        ))
        db.send_create_signal('whs', ['Pallet'])

        # Adding model 'Inventory'
        db.create_table('whs_inventory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 7, 18, 0, 0))),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('whs', ['Inventory'])

        # Adding model 'OldBrick'
        db.create_table('whs_oldbrick', (
            ('brick_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['whs.Brick'], unique=True, primary_key=True)),
            ('old', self.gf('django.db.models.fields.IntegerField')()),
            ('prim', self.gf('django.db.models.fields.CharField')(default='', max_length=260)),
        ))
        db.send_create_signal('whs', ['OldBrick'])

        # Adding model 'Sold'
        db.create_table('whs_sold', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brick_from', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sold_brick_from', null=True, to=orm['whs.Brick'])),
            ('batch_from', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=600, null=True, blank=True)),
            ('brick', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sold_brick', to=orm['whs.Brick'])),
            ('batch', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('tara', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
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

        # Adding model 'Man'
        db.create_table('whs_man', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 7, 18, 0, 0), unique=True)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('whs', ['Man'])

        # Adding model 'BuhAgent'
        db.create_table('whs_buhagent', (
            ('agent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['whs.Agent'], unique=True, primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=11)),
        ))
        db.send_create_signal('whs', ['BuhAgent'])

        # Adding model 'Brick'
        db.create_table('whs_brick', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cavitation', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('color', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('mark', self.gf('django.db.models.fields.PositiveIntegerField')(default=100)),
            ('width', self.gf('django.db.models.fields.FloatField')(default=1.4)),
            ('view', self.gf('django.db.models.fields.CharField')(default=u'\u041b', max_length=60)),
            ('ctype', self.gf('django.db.models.fields.CharField')(default='', max_length=6, blank=True)),
            ('defect', self.gf('django.db.models.fields.CharField')(default=u'', max_length=60, blank=True)),
            ('refuse', self.gf('django.db.models.fields.CharField')(default=u'', max_length=10, blank=True)),
            ('features', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=160)),
            ('css', self.gf('django.db.models.fields.CharField')(default=u'', max_length=360)),
            ('label', self.gf('django.db.models.fields.CharField')(default='', max_length=660)),
            ('total', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('nomenclature', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['whs.Nomenclature'], null=True, blank=True)),
        ))
        db.send_create_signal('whs', ['Brick'])

        # Adding model 'Bill'
        db.create_table('whs_bill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 7, 18, 0, 0))),
            ('agent', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'bill_agents', to=orm['whs.Agent'])),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(default=350, related_name='bill_sallers', to=orm['whs.Seller'])),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('whs', ['Bill'])

        # Adding model 'Seller'
        db.create_table('whs_seller', (
            ('agent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['whs.Agent'], unique=True, primary_key=True)),
            ('director_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('director', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('buhgalter_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('buhgalter', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('dispetcher_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('dispetcher', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('nds', self.gf('django.db.models.fields.FloatField')(default=0.18)),
        ))
        db.send_create_signal('whs', ['Seller'])

    def backwards(self, orm):
        # Deleting model 'Add'
        db.delete_table('whs_add')

        # Deleting model 'Write_off'
        db.delete_table('whs_write_off')

        # Deleting model 'Price'
        db.delete_table('whs_price')

        # Deleting model 'Sorting'
        db.delete_table('whs_sorting')

        # Deleting model 'Agent'
        db.delete_table('whs_agent')

        # Deleting model 'OldAgent'
        db.delete_table('whs_oldagent')

        # Deleting model 'Pallet'
        db.delete_table('whs_pallet')

        # Deleting model 'Inventory'
        db.delete_table('whs_inventory')

        # Deleting model 'OldBrick'
        db.delete_table('whs_oldbrick')

        # Deleting model 'Sold'
        db.delete_table('whs_sold')

        # Deleting model 'Nomenclature'
        db.delete_table('whs_nomenclature')

        # Deleting model 'Man'
        db.delete_table('whs_man')

        # Deleting model 'BuhAgent'
        db.delete_table('whs_buhagent')

        # Deleting model 'Brick'
        db.delete_table('whs_brick')

        # Deleting model 'Bill'
        db.delete_table('whs_bill')

        # Deleting model 'Seller'
        db.delete_table('whs_seller')

    models = {
        'lab.batch': {
            'Meta': {'object_name': 'Batch'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'chamfer': ('django.db.models.fields.IntegerField', [], {}),
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 18, 0, 0)'}),
            'density': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.Density']"}),
            'efflorescence': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.Efflorescence']", 'null': 'True', 'blank': 'True'}),
            'flexion': ('django.db.models.fields.FloatField', [], {}),
            'frost_resistance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.FrostResistance']", 'null': 'True', 'blank': 'True'}),
            'heatconduction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.HeatConduction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'mark': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pressure': ('django.db.models.fields.FloatField', [], {}),
            'seonr': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.SEONR']"}),
            'tto': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'water_absorption': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.WaterAbsorption']", 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.FloatField', [], {'max_length': '30'})
        },
        'lab.density': {
            'Meta': {'object_name': 'Density'},
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 18, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.efflorescence': {
            'Meta': {'object_name': 'Efflorescence'},
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 18, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'})
        },
        'lab.frostresistance': {
            'Meta': {'object_name': 'FrostResistance'},
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 18, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.heatconduction': {
            'Meta': {'object_name': 'HeatConduction'},
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 18, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.part': {
            'Meta': {'object_name': 'Part'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab.Batch']"}),
            'cause': ('django.db.models.fields.TextField', [], {'max_length': '600'}),
            'defect': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'dnumber': ('django.db.models.fields.FloatField', [], {}),
            'half': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'test': ('django.db.models.fields.IntegerField', [], {}),
            'tto': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '30'})
        },
        'lab.seonr': {
            'Meta': {'object_name': 'SEONR'},
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 18, 0, 0)'}),
            'delta': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {})
        },
        'lab.waterabsorption': {
            'Meta': {'object_name': 'WaterAbsorption'},
            'color': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 18, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {})
        },
        'whs.add': {
            'Meta': {'ordering': "('-doc__date',)", 'object_name': 'Add'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'man'", 'to': "orm['whs.Brick']"}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'add'", 'to': "orm['whs.Man']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'part': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'add'", 'to': "orm['lab.Part']"})
        },
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'rs': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '600', 'blank': 'True'})
        },
        'whs.bill': {
            'Meta': {'ordering': "['-date', '-number']", 'object_name': 'Bill'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'bill_agents'", 'to': "orm['whs.Agent']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 18, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'default': '350', 'related_name': "'bill_sallers'", 'to': "orm['whs.Seller']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'})
        },
        'whs.brick': {
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
            'nomenclature': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['whs.Nomenclature']", 'null': 'True', 'blank': 'True'}),
            'refuse': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '10', 'blank': 'True'}),
            'total': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'view': ('django.db.models.fields.CharField', [], {'default': "u'\\u041b'", 'max_length': '60'}),
            'width': ('django.db.models.fields.FloatField', [], {'default': '1.4'})
        },
        'whs.buhagent': {
            'Meta': {'ordering': "('name',)", 'object_name': 'BuhAgent', '_ormbases': ['whs.Agent']},
            'agent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['whs.Agent']", 'unique': 'True', 'primary_key': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'})
        },
        'whs.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 18, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'})
        },
        'whs.man': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Man'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 18, 0, 0)', 'unique': 'True'}),
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
            'Meta': {'ordering': "('name',)", 'object_name': 'OldAgent', '_ormbases': ['whs.Agent']},
            'agent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['whs.Agent']", 'unique': 'True', 'primary_key': 'True'}),
            'old': ('django.db.models.fields.IntegerField', [], {})
        },
        'whs.oldbrick': {
            'Meta': {'ordering': "('-width', 'color', '-view', 'ctype', 'defect', 'features', 'mark', 'refuse', 'id')", 'object_name': 'OldBrick', '_ormbases': ['whs.Brick']},
            'brick_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['whs.Brick']", 'unique': 'True', 'primary_key': 'True'}),
            'old': ('django.db.models.fields.IntegerField', [], {}),
            'prim': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '260'})
        },
        'whs.pallet': {
            'Meta': {'object_name': 'Pallet'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pallets'", 'to': "orm['whs.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'poddon': ('django.db.models.fields.PositiveIntegerField', [], {'default': '352'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': '200'})
        },
        'whs.price': {
            'Meta': {'object_name': 'Price'},
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['whs.Brick']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {})
        },
        'whs.seller': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Seller', '_ormbases': ['whs.Agent']},
            'agent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['whs.Agent']", 'unique': 'True', 'primary_key': 'True'}),
            'buhgalter': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'buhgalter_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'director': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'director_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'dispetcher': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'dispetcher_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nds': ('django.db.models.fields.FloatField', [], {'default': '0.18'})
        },
        'whs.sold': {
            'Meta': {'ordering': "['-doc__date', '-doc__number']", 'object_name': 'Sold'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'batch': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'batch_from': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '600', 'null': 'True', 'blank': 'True'}),
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sold_brick'", 'to': "orm['whs.Brick']"}),
            'brick_from': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sold_brick_from'", 'null': 'True', 'to': "orm['whs.Brick']"}),
            'delivery': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'solds'", 'to': "orm['whs.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'tara': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'whs.sorting': {
            'Meta': {'object_name': 'Sorting'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sorting'", 'to': "orm['lab.Batch']"}),
            'brick': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sorting'", 'to': "orm['whs.Brick']"}),
            'brick_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sorting_from'", 'to': "orm['whs.Brick']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 18, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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