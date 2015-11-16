# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field missing_ministers on 'Meeting'
        m2m_table_name = db.shorten_name(u'committeeVotes_meeting_missing_ministers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meeting', models.ForeignKey(orm[u'committeeVotes.meeting'], null=False)),
            ('minister', models.ForeignKey(orm[u'committeeVotes.minister'], null=False))
        ))
        db.create_unique(m2m_table_name, ['meeting_id', 'minister_id'])


    def backwards(self, orm):
        # Removing M2M table for field missing_ministers on 'Meeting'
        db.delete_table(db.shorten_name(u'committeeVotes_meeting_missing_ministers'))


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
            'missing_ministers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'meeting_missing_minister'", 'blank': 'True', 'to': u"orm['committeeVotes.Minister']"}),
            'proposed_bills': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['committeeVotes.Bill']", 'symmetrical': 'False', 'blank': 'True'}),
            'took_place': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            'voting_ministers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'meeting_voting_minister'", 'blank': 'True', 'to': u"orm['committeeVotes.Minister']"})
        },
        u'committeeVotes.minister': {
            'Meta': {'object_name': 'Minister'},
            'coop': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'oknesset': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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