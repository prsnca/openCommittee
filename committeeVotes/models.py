from django.db import models

# Create your models here.
class Bill(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    def __unicode__(self):
        return self.name

class VoteType(models.Model):
    typeName = models.CharField(max_length=10)
    def __unicode__(self):
        return self.typeName

class Meeting(models.Model):
    took_place = models.DateField()
    proposed_bills = models.ManyToManyField(Bill, blank=True)
    def __unicode__(self):
        return "Meeting #" + str(self.id) + u" - %s" % self.took_place

class Minister(models.Model):
    name = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name

class Vote(models.Model):
    vote = models.ForeignKey(VoteType)
    meeting = models.ForeignKey(Meeting)
    bill = models.ForeignKey(Bill)
    minister = models.ForeignKey(Minister)

    def __unicode__(self):
        return self.minister.name + " voted " + self.vote.typeName




