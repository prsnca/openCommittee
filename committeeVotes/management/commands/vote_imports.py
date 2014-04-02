# coding: utf-8
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from committeeVotes.models import Bill, Minister, Vote, Meeting, VoteType
from django.core.exceptions import ValidationError
import csv, os, shutil, re, sys, codecs
from django.core.files import File
from django.core.management import call_command
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned


from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "committeeVotes.settings") # Replace with your app name.

def get_meeting(date):
    try:
        meeting = Meeting.objects.get(took_place=date)
    except ObjectDoesNotExist:
        print "Meeting was not found!"
        return None
    return meeting

def get_bill(name):
    try:
        bill = Bill.objects.get(name=name)
    except ObjectDoesNotExist:
        print "Bill was not found!"
        return None
    return bill

def get_minister(name):
    try:
        minister = Minister.objects.get(name=name)
    except ObjectDoesNotExist:
        print "Minister was not found!"
        return None
    return minister

def get_voteType(voteT):
    try:
        vote = VoteType.objects.get(typeName=voteT)
    except ObjectDoesNotExist:
        print "Vote type was not found!"
        return None
    return vote

VOTE_FIELDS = [
    ('meeting', get_meeting),
    ('bill', get_bill),
    ('minister', get_minister),
    ('vote', get_voteType)
]


#
# #Importing bills CSV
class Command(BaseCommand):
    def handle(self, *args, **options):

        #args = '<filename>'
        help = 'Parses the CSV to votes'

        print args[0]

        if len(args) <= 0:
            raise CommandError('Please specify file name')

        if not os.path.exists(args[0]):
            raise CommandError("File %s doesn't exist" % args[0])
        #with codecs.open(args[0], 'r', 'cp1255 ') as f:
        with open(args[0], 'r') as f:
            r = csv.DictReader(f)

            for d in r:
                vote = Vote()
                for header, conv_func in VOTE_FIELDS:
                    value = d[header]
                    value = conv_func(value)
                    if value:
                        setattr(vote, header, value)
                    else:
                        print "error in header " + str(header)
                        continue
                try:
                    vote.full_clean()
                except ValidationError:
                    print "error in vote"
                    continue

                vote.save()

        print 'Done importing votes csv!'

