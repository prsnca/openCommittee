# -*- coding: utf-8 -*-
import argparse
import requests
import re
import json
import os
from django.core.management import BaseCommand
from optparse import make_option
OPENLAW_API_URL = 'http://tools.openlaw.org.il/openlaw/clear'

OKNESSET_MEMBER_API_URL = 'https://oknesset.org/api/v2/member/'

PATTERNS_TO_REMOVE = [r'-[0-9]-']

TEXTS_TO_REMOVE = [u"בישיבה יורשו להשתתף מוזמנים שנוכחותם חיונית והשתתפותם אושרה על-ידי מזכירות",
                   u"-------------------------------------------------------------", u"הממשלה", u'מספר נספח', u'השר המגיש', u'המשך הדיון', u'המשך הדין']


def get_minister_names():
    ministers_dict = json.loads(requests.get(OKNESSET_MEMBER_API_URL).text)
    return [minister["name"]
            for minister in ministers_dict["objects"]]


def write_to(filename, content):
    with open(filename, 'w') as file:
        file.write(content.encode('utf8'))


def generate_hebrew_numerals(up_to):
    # Works up to 100; no need for more.
    alef_bet = [unichr(letter_idx)
                for letter_idx in range(ord(u'א'), ord(u'ת') + 1) if unichr(letter_idx) not in [u'ך', u'ן', u'ץ', u'ם', u'ף']]
    hebrew_numerals = []
    # טו and טז
    special_cases = {
        15: u'טו',
        16: u'טז'
    }
    for n in range(1, up_to + 1):
        if n in special_cases:
            hebrew_numerals.append(special_cases[n])
        elif n < 11:
            hebrew_numerals.append(alef_bet[n - 1])
        else:
            hebrew_numerals.append(
                alef_bet[10 + n / 10 - 2] + (alef_bet[n % 10 - 1] if n % 10 > 0 else ''))
    return hebrew_numerals

ALEF_BET = generate_hebrew_numerals(100)


def get_pdf_text(pdf_url):
    return requests.post(OPENLAW_API_URL, data=dict(url=pdf_url)).text


def clean_pdf_text(text, texts_to_remove=TEXTS_TO_REMOVE, patterns_to_remove=PATTERNS_TO_REMOVE):
    """ Remove all unneccessary clutter from the text. """
    cleaned_text = text
    print type(cleaned_text)
    for text_to_remove in texts_to_remove:
        cleaned_text = cleaned_text.replace(text_to_remove, u'')
    for pattern_to_remove in patterns_to_remove:
        cleaned_text = re.sub(pattern_to_remove, '', cleaned_text)
    # A hack to swap round brackets.
    brackets_dict = {u'(': u')', u')': u'('}
    cleaned_text = re.sub(r'(\(|\))', lambda m: brackets_dict[
                          m.string[m.start():m.end()]], cleaned_text)
    return cleaned_text


def get_raw_topics(committee_schedule_text):
    raw_topics = []
    current_topic = ""
    should_parse_topic = False
    current_topic_letter_idx = 0
    schedule_lines = committee_schedule_text.splitlines()
    beggining_of_new_topic = ""
    for line in schedule_lines:
        beggining_of_new_topic = ALEF_BET[current_topic_letter_idx] + '.'
        if line.lstrip().startswith(beggining_of_new_topic):
            current_topic_letter_idx += 1
            raw_topics.append(current_topic)
            current_topic = line.replace(beggining_of_new_topic, '')
            should_parse_topic = True
        elif should_parse_topic:
            current_topic += line + '\n'
    raw_topics.append(current_topic)
    return raw_topics


def get_topics(raw_topics):
    topics = []
    topic = None
    spaces_regex = r' {3,4}'
    for raw_topic in raw_topics:
        topic = raw_topic
        # remove empty lines
        topic = os.linesep.join([s for s in topic.splitlines() if s.strip()])
        # remove reduntant spacing at row beginning and end
        topic = os.linesep.join([s.lstrip().rstrip()
                                 for s in topic.splitlines()])
        # remove newlines
        topic = topic.replace(os.linesep, ' ')
        topic = re.sub(r'([^\s])\(', r'\1 (', topic)
        # remove everything after the comma
        topic_splitted = topic.split(u', התש')
        if len(topic_splitted) > 0:
            topic = topic_splitted[0]
        # Whenever there are 4 or 3 consequent spaces,make it one.
        #topic = re.sub(spaces_regex, ' ', topic)
        topics.append(topic)
    return topics


def get_committee_schedule(pdf_url, remove_minister_names):
    pdf_text = get_pdf_text(pdf_url)
    texts_to_remove = TEXTS_TO_REMOVE + \
        ([u'ואחרים'] + get_minister_names() if remove_minister_names else [])
    patterns_to_remove = PATTERNS_TO_REMOVE + \
        ([re.compile(u'של.חה"כ', re.DOTALL)] if remove_minister_names else [])
    cleaned_pdf_text = clean_pdf_text(
        pdf_text, texts_to_remove=texts_to_remove, patterns_to_remove=patterns_to_remove)
    raw_topics = get_raw_topics(cleaned_pdf_text)
    return get_topics(raw_topics)

class Command(BaseCommand):
    help = 'Fetch and parse the committee schedule from the schedule pdf.'

    def parse_date(option, opt_str, value, parser):
        try:
            setattr(parser.values, option.dest,
                    datetime.datetime.strptime(value, DATE_FORMAT).date())
        except ValueError:
            return

    option_list = BaseCommand.option_list + (
        make_option('-u', '--url', dest="url", type=str,
                    help="URL of the pdf."),
        make_option('-f', '--file', help="Output file",
                    type=str, default="out.txt"),
        make_option('-r', '--remove-ministers',
                    help="Should remove minister names from committee schedule", action='store_true')
    )

    def handle(self, *args, **options):
        if options['url'] is None:
            print "PDF URL is required."
            return
        committee_schedule = get_committee_schedule(
            options['url'], options['remove_ministers'])
        write_to(options['file'], "\n-------------------\n".join([x for x in
                                                                  committee_schedule]))