from django.db import models

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

class Meeting(models.Model):
    took_place = models.DateField(unique=True)
    proposed_bills = models.ManyToManyField(Bill, blank=True)
    def __unicode__(self):
        return "Meeting #" + str(self.id) + u" - %s" % self.took_place

class Minister(models.Model):
    name = models.CharField(max_length=30)
    photo = models.CharField(max_length=100)
    mail = models.EmailField(null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    coop = models.NullBooleanField(blank=True)
    def __unicode__(self):
        return self.name

class Vote(models.Model):
    vote = models.ForeignKey(VoteType)
    meeting = models.ForeignKey(Meeting)
    bill = models.ForeignKey(Bill)
    minister = models.ForeignKey(Minister, related_name="votes")

    class Meta:
        unique_together = ("bill","minister")

    def __unicode__(self):
        return self.minister.name + " voted " + self.vote.typeName




