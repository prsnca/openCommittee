# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Bill'
        db.create_table(u'committeeVotes_bill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('oknesset_url', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('passed', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'committeeVotes', ['Bill'])

        # Adding model 'VoteType'
        db.create_table(u'committeeVotes_votetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('typeName', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'committeeVotes', ['VoteType'])

        # Adding model 'Meeting'
        db.create_table(u'committeeVotes_meeting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('took_place', self.gf('django.db.models.fields.DateField')(unique=True)),
        ))
        db.send_create_signal(u'committeeVotes', ['Meeting'])

        # Adding M2M table for field proposed_bills on 'Meeting'
        m2m_table_name = db.shorten_name(u'committeeVotes_meeting_proposed_bills')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meeting', models.ForeignKey(orm[u'committeeVotes.meeting'], null=False)),
            ('bill', models.ForeignKey(orm[u'committeeVotes.bill'], null=False))
        ))
        db.create_unique(m2m_table_name, ['meeting_id', 'bill_id'])

        # Adding model 'Minister'
        db.create_table(u'committeeVotes_minister', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('photo', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'committeeVotes', ['Minister'])

        # Adding model 'Vote'
        db.create_table(u'committeeVotes_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['committeeVotes.VoteType'])),
            ('meeting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['committeeVotes.Meeting'])),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['committeeVotes.Bill'])),
            ('minister', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['committeeVotes.Minister'])),
        ))
        db.send_create_signal(u'committeeVotes', ['Vote'])

        # Adding unique constraint on 'Vote', fields ['bill', 'minister']
        db.create_unique(u'committeeVotes_vote', ['bill_id', 'minister_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Vote', fields ['bill', 'minister']
        db.delete_unique(u'committeeVotes_vote', ['bill_id', 'minister_id'])

        # Deleting model 'Bill'
        db.delete_table(u'committeeVotes_bill')

        # Deleting model 'VoteType'
        db.delete_table(u'committeeVotes_votetype')

        # Deleting model 'Meeting'
        db.delete_table(u'committeeVotes_meeting')

        # Removing M2M table for field proposed_bills on 'Meeting'
        db.delete_table(db.shorten_name(u'committeeVotes_meeting_proposed_bills'))

        # Deleting model 'Minister'
        db.delete_table(u'committeeVotes_minister')

        # Deleting model 'Vote'
        db.delete_table(u'committeeVotes_vote')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'photo': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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