# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Agent'
        db.create_table('agent_agent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('inn', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('kpp', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('bank', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('ks', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('bic', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('rs', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('agent', ['Agent'])

        # Adding model 'Seller'
        db.create_table('agent_seller', (
            ('agent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['agent.Agent'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('agent', ['Seller'])


    def backwards(self, orm):
        
        # Deleting model 'Agent'
        db.delete_table('agent_agent')

        # Deleting model 'Seller'
        db.delete_table('agent_seller')


    models = {
        'agent.agent': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Agent'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'bank': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'bic': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inn': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'kpp': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'ks': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'rs': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'agent.seller': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Seller', '_ormbases': ['agent.Agent']},
            'agent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['agent.Agent']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['agent']
