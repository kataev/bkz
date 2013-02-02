# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Warren'
        db.delete_table('make_warren')

        # Deleting model 'TTS'
        db.delete_table('make_tts')

        # Deleting field 'Forming.timestamp'
        db.delete_column('make_forming', 'timestamp')

        # Adding field 'Forming.tts'
        db.add_column('make_forming', 'tts',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=20),
                      keep_default=False)

        # Adding field 'Forming.density'
        db.add_column('make_forming', 'density',
                      self.gf('django.db.models.fields.FloatField')(default=3),
                      keep_default=False)

        # Adding field 'Forming.sand'
        db.add_column('make_forming', 'sand',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Forming.k'
        db.add_column('make_forming', 'k',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Forming.stratcher'
        db.add_column('make_forming', 'stratcher',
                      self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=300, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Forming.poke'
        db.add_column('make_forming', 'poke',
                      self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=300, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Forming.temperature'
        db.alter_column('make_forming', 'temperature', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Forming.humidity'
        db.alter_column('make_forming', 'humidity', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Forming.size'
        db.alter_column('make_forming', 'size', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))
    def backwards(self, orm):
        # Adding model 'Warren'
        db.create_table('make_warren', (
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='consumer', null=True, to=orm['make.Warren'], blank=True)),
            ('amount', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('tts', self.gf('django.db.models.fields.related.ForeignKey')(related_name='warrens', null=True, to=orm['make.TTS'], blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 18, 0, 0), null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('part', self.gf('django.db.models.fields.related.ForeignKey')(related_name='warrens', null=True, to=orm['lab.Part'], blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('make', ['Warren'])

        # Adding model 'TTS'
        db.create_table('make_tts', (
            ('forming', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tts', null=True, to=orm['make.Forming'], blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('make', ['TTS'])


        # User chose to not deal with backwards NULL issues for 'Forming.timestamp'
        raise RuntimeError("Cannot reverse this migration. 'Forming.timestamp' and its values cannot be restored.")
        # Deleting field 'Forming.tts'
        db.delete_column('make_forming', 'tts')

        # Deleting field 'Forming.density'
        db.delete_column('make_forming', 'density')

        # Deleting field 'Forming.sand'
        db.delete_column('make_forming', 'sand')

        # Deleting field 'Forming.k'
        db.delete_column('make_forming', 'k')

        # Deleting field 'Forming.stratcher'
        db.delete_column('make_forming', 'stratcher')

        # Deleting field 'Forming.poke'
        db.delete_column('make_forming', 'poke')


        # User chose to not deal with backwards NULL issues for 'Forming.temperature'
        raise RuntimeError("Cannot reverse this migration. 'Forming.temperature' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Forming.humidity'
        raise RuntimeError("Cannot reverse this migration. 'Forming.humidity' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Forming.size'
        raise RuntimeError("Cannot reverse this migration. 'Forming.size' and its values cannot be restored.")
    models = {
        'make.forming': {
            'Meta': {'object_name': 'Forming'},
            'cavitation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 2, 3, 0, 0)'}),
            'density': ('django.db.models.fields.FloatField', [], {}),
            'humidity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'k': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'poke': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'sand': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'stratcher': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'tts': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'vacuum': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['whs.Width']"})
        },
        'whs.width': {
            'Meta': {'ordering': "('pk',)", 'object_name': 'Width'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'type': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['make']