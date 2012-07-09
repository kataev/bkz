# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Device'
        db.create_table('it_device', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['it.Device'], null=True, blank=True)),
        ))
        db.send_create_signal('it', ['Device'])

        # Adding model 'Buy'
        db.create_table('it_buy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cartridge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['it.Device'])),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 6, 26, 0, 0))),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=600, blank=True)),
        ))
        db.send_create_signal('it', ['Buy'])

        # Adding model 'Plug'
        db.create_table('it_plug', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cartrige', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'catridge', to=orm['it.Device'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'printer', to=orm['it.Device'])),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 6, 26, 0, 0))),
        ))
        db.send_create_signal('it', ['Plug'])

        # Adding model 'Work'
        db.create_table('it_work', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['it.Device'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 6, 26, 0, 0))),
            ('people', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default=u'info', max_length=300)),
            ('date_finished', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('it', ['Work'])

    def backwards(self, orm):
        # Deleting model 'Device'
        db.delete_table('it_device')

        # Deleting model 'Buy'
        db.delete_table('it_buy')

        # Deleting model 'Plug'
        db.delete_table('it_plug')

        # Deleting model 'Work'
        db.delete_table('it_work')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'it.buy': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Buy'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cartridge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['it.Device']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 6, 26, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '600', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {})
        },
        'it.device': {
            'Meta': {'object_name': 'Device'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['it.Device']", 'null': 'True', 'blank': 'True'})
        },
        'it.plug': {
            'Meta': {'object_name': 'Plug'},
            'cartrige': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'catridge'", 'to': "orm['it.Device']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 6, 26, 0, 0)'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'printer'", 'to': "orm['it.Device']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'it.work': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Work'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 6, 26, 0, 0)'}),
            'date_finished': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['it.Device']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'people': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'info'", 'max_length': '300'})
        }
    }

    complete_apps = ['it']