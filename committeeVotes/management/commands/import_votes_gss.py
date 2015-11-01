# coding: utf-8
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from committeeVotes.models import Bill, Minister, Vote, Meeting, VoteType
from django.core.exceptions import ValidationError
import csv, os, shutil, re, sys, codecs, urllib, json, datetime
from django.core.files import File
from django.core.management import call_command
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned


from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "committeeVotes.settings") # Replace with your app name.

URL = "https://spreadsheets.google.com/feeds/list/1KNFehdsumR-GVq4hlHUC7h2lfGwFKk-7pwluwdykL-w/3/public/values?alt=json"

def get_meeting(date):
    try:
        d = datetime.datetime.strptime(date + ' 00:00:00', '%m/%d/%Y %H:%M:%S').date()
        meeting = Meeting.objects.get_or_create(took_place=d)
        print "got meeting!"
    except MultipleObjectsReturned:
        print "Few meetings were found!"
        return None
    return meeting[0]

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

        help = 'Imports votes from google spreadsheet to "Votes" table'

        response = urllib.urlopen(URL);
        data = json.loads(response.read())

        votes = data['feed']['entry']

        for e in votes:
            vote = Vote()
            for header, conv_func in VOTE_FIELDS:
                value = e['gsx$' + header]['$t']
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
            try:
                vote.meeting.proposed_bills.add(vote.bill)
            except:
                print "error in adding bill to meeting"
                continue
            try:
                vote.meeting.voting_ministers.add(vote.minister)
            except:
                print "error in adding minister to meeting"
                continue
            if not Vote.objects.filter(bill=vote.bill, minister=vote.minister).count() == 0:
                print "Vote already exists!"
            else:
                vote.save()
                print "Vote saved!"

        print 'Done importing votes from google spreadsheet!!'


