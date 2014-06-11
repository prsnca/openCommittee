# coding: utf-8
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from committeeVotes.models import Bill
from django.core.exceptions import ValidationError
import csv, os, shutil, re, sys, codecs
from django.core.files import File
from django.core.management import call_command
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned


from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "committeeVotes.settings") # Replace with your app name.

def vote_to_bool(vote):
    if not vote or vote == '':
        return None
    if vote == 'בעד':
        return True
    elif vote == 'נגד':
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

        #args = '<filename>'
        help = 'Bills places from csv file to "Bills" table'

        print args[0]

        if len(args) <= 0:
            raise CommandError('Please specify file name')

        if not os.path.exists(args[0]):
            raise CommandError("File %s doesn't exist" % args[0])
        #with codecs.open(args[0], 'r', 'cp1255 ') as f:
        with open(args[0], 'r') as f:
            r = csv.DictReader(f)

            for d in r:
                bill = Bill()
                for header, conv_func in BILL_FIELDS:
                    value = d[header]
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
        print 'Done importing bills csv!'

