# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Agent'
        db.delete_table('buh_agent')

        # Adding model 'BuxAgent'
        db.create_table('buh_buxagent', (
            ('agent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['agent.Agent'], unique=True, primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=11)),
        ))
        db.send_create_signal('buh', ['BuxAgent'])


    def backwards(self, orm):
        
        # Adding model 'Agent'
        db.create_table('buh_agent', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=11, unique=True)),
            ('agent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['agent.Agent'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('buh', ['Agent'])

        # Deleting model 'BuxAgent'
        db.delete_table('buh_buxagent')


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
        'buh.buxagent': {
            'Meta': {'ordering': "('name',)", 'object_name': 'BuxAgent', '_ormbases': ['agent.Agent']},
            'agent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['agent.Agent']", 'unique': 'True', 'primary_key': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'})
        },
        'buh.nomenclature': {
            'Meta': {'object_name': 'Nomenclature'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['buh']
