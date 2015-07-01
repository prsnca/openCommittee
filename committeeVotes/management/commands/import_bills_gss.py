# coding: utf-8
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from committeeVotes.models import Bill
from django.core.exceptions import ValidationError
import csv, os, shutil, re, sys, codecs
from django.core.files import File
from django.core.management import call_command
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
import urllib, json
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "committeeVotes.settings") # Replace with your app name.

URL = "https://spreadsheets.google.com/feeds/list/1KNFehdsumR-GVq4hlHUC7h2lfGwFKk-7pwluwdykL-w/2/public/values?alt=json"



def vote_to_bool(vote):
    if not vote or vote == '':
        return None
    if vote == u'בעד':
        return True
    elif vote == u'נגד':
        return False

BILL_FIELDS = [
    ('name', None),
    ('oknesset_url', None),
    ('passed', vote_to_bool)
]


#
# #Importing bills CSV
class Command(BaseCommand):
    def handle(self, *args, **options):

        help = 'Bills places from google spreadsheet to "Bills" table'

        response = urllib.urlopen(URL);
        data = json.loads(response.read())

        bills = data['feed']['entry']

        for e in bills:
            bill = Bill()
            for header, conv_func in BILL_FIELDS:
                value = e['gsx$' + header.replace("_","")]['$t']
                if conv_func:
                    value = conv_func(value)
                setattr(bill, header, value)
            try:
                bill.full_clean()
            except ValidationError as e:
                print "error in bill"
                continue

            if not Bill.objects.filter(name=bill.name).count() == 0:
                print "Bill already exists!"
            else:
                bill.save()
                print "Bill saved!"
        print 'Done importing bills from google spreadsheet!'

