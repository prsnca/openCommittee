# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Minister.mail'
        db.add_column(u'committeeVotes_minister', 'mail',
                      self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Minister.facebook'
        db.add_column(u'committeeVotes_minister', 'facebook',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Minister.twitter'
        db.add_column(u'committeeVotes_minister', 'twitter',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Minister.phone'
        db.add_column(u'committeeVotes_minister', 'phone',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Minister.mail'
        db.delete_column(u'committeeVotes_minister', 'mail')

        # Deleting field 'Minister.facebook'
        db.delete_column(u'committeeVotes_minister', 'facebook')

        # Deleting field 'Minister.twitter'
        db.delete_column(u'committeeVotes_minister', 'twitter')

        # Deleting field 'Minister.phone'
        db.delete_column(u'committeeVotes_minister', 'phone')


    models = {
        u'committeeVotes.bill': {
            'Meta': {'object_name': 'Bill'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'oknesset_url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'passed': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        u'committeeVotes.meeting': {
            'Meta': {'object_name': 'Meeting'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposed_bills': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['committeeVotes.Bill']", 'symmetrical': 'False', 'blank': 'True'}),
            'took_place': ('django.db.models.fields.DateField', [], {'unique': 'True'})
        },
        u'committeeVotes.minister': {
            'Meta': {'object_name': 'Minister'},
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'committeeVotes.vote': {
            'Meta': {'unique_together': "(('bill', 'minister'),)", 'object_name': 'Vote'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['committeeVotes.Bill']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['committeeVotes.Meeting']"}),
            'minister': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': u"orm['committeeVotes.Minister']"}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['committeeVotes.VoteType']"})
        },
        u'committeeVotes.votetype': {
            'Meta': {'object_name': 'VoteType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'typeName': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['committeeVotes']