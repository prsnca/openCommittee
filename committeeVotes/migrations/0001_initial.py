# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('oknesset_url', models.CharField(max_length=100, null=True, blank=True)),
                ('passed', models.NullBooleanField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('took_place', models.DateField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Minister',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('photo', models.CharField(max_length=100, null=True, blank=True)),
                ('mail', models.EmailField(max_length=75, null=True, blank=True)),
                ('facebook', models.CharField(max_length=100, null=True, blank=True)),
                ('twitter', models.CharField(max_length=100, null=True, blank=True)),
                ('phone', models.CharField(max_length=20, null=True, blank=True)),
                ('oknesset', models.CharField(max_length=100, null=True, blank=True)),
                ('coop', models.NullBooleanField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bill', models.ForeignKey(to='committeeVotes.Bill')),
                ('meeting', models.ForeignKey(to='committeeVotes.Meeting')),
                ('minister', models.ForeignKey(related_name='votes', to='committeeVotes.Minister')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VoteType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('typeName', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='vote',
            name='vote',
            field=models.ForeignKey(to='committeeVotes.VoteType'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('bill', 'minister')]),
        ),
        migrations.AddField(
            model_name='meeting',
            name='missing_ministers',
            field=models.ManyToManyField(related_name='meeting_missing_minister', to='committeeVotes.Minister', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='proposed_bills',
            field=models.ManyToManyField(to='committeeVotes.Bill', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='voting_ministers',
            field=models.ManyToManyField(related_name='meeting_voting_minister', to='committeeVotes.Minister', blank=True),
            preserve_default=True,
        ),
    ]
