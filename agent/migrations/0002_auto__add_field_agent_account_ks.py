# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Agent.account_ks'
        db.add_column('agent_agent', 'account_ks', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Agent.account_ks'
        db.delete_column('agent_agent', 'account_ks')


    models = {
        'agent.agent': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Agent'},
            'account': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'account_ks': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'bank': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'form': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inn': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['agent']
