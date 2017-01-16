# coding: utf-8

from django.db import models
from django.conf import settings
# Create your models here.
class Bill(models.Model):
    name = models.CharField(max_length=500)
    oknesset_url = models.CharField(max_length=100, blank=True, null=True)
    passed = models.NullBooleanField()
    def __unicode__(self):
        return self.name

class VoteType(models.Model):
    typeName = models.CharField(max_length=10)
    def __unicode__(self):
        return self.typeName

class Minister(models.Model):
    name = models.CharField(max_length=30)
    title = models.CharField(max_length=100, null=True, blank=True)
    photo = models.CharField(max_length=100, null=True, blank=True)
    mail = models.EmailField(null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    oknesset = models.CharField(max_length=100, null=True, blank=True)
    coop = models.NullBooleanField(blank=True)
    @property
    def photo_url(self):
        url_prefix=""
        if 'http' not in self.photo:
            url_prefix=settings.MEDIA_URL
        return "{prefix}{photo}.jpg".format(prefix=url_prefix,photo=self.photo)
    def __unicode__(self):
        return self.name

class Meeting(models.Model):
    took_place = models.DateField(unique=True)
    proposed_bills = models.ManyToManyField(Bill, blank=True)
    voting_ministers = models.ManyToManyField(Minister, blank=True, related_name='meeting_voting_minister')
    missing_ministers = models.ManyToManyField(Minister, blank=True, related_name='meeting_missing_minister')
    def __unicode__(self):
        return "Meeting #" + str(self.id) + u" - %s" % self.took_place

class Vote(models.Model):
    vote = models.ForeignKey(VoteType)
    meeting = models.ForeignKey(Meeting)
    bill = models.ForeignKey(Bill, related_name="votes")
    minister = models.ForeignKey(Minister, related_name="votes")

    class Meta:
        unique_together = ("bill","minister")

    def __unicode__(self):
        return self.minister.name + " voted " + self.vote.typeName