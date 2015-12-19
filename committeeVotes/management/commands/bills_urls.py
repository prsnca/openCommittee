# coding: utf-8
import requests
import json
import Levenshtein
from collections import namedtuple
from oauth2client.client import SignedJwtAssertionCredentials
import gspread
from jinja2 import Environment, FileSystemLoader
import datetime
import SimpleHTTPServer
import SocketServer
from django.core.management import BaseCommand
from optparse import make_option
import webbrowser
import os
import threading

OKNESSET_BILL_API_URL = 'https://oknesset.org/api/v2/bill/?order_by=-stage_date&limit=1000'

OCOMMITTEE_SPREADSHEET_NAME = u"הצעות חוק 2015"

MEETING_DATE_COLUMN_INDEX = 1

DATE_FORMAT = "%m/%d/%Y"

RESOURCES_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "bills_urls_resources")

CREDENTAIALS_FILE = RESOURCES_PATH + "/credentials.json"

EXECUTION_CREDENTIALS_FILE = RESOURCES_PATH + "/execute_api_credentials.json"

STOP_WORDS = [u"חוק", u"תיקון", u"הצעת", u"רציפות"]

TEMPLATE_FILENAME = "bills_template.html"

RENDERED_OUTPUT_PATH = RESOURCES_PATH + "/bills.html"

Bill = namedtuple("Bill", "id name oknesset_url oknesset_name match_ratio")


def get_all_oknesset_bills():
    bills = []
    current_bills, next_bills_api_url = get_next_oknesset_bills(
        OKNESSET_BILL_API_URL)
    bills.extend(current_bills)
    while next_bills_api_url is not None:
        current_bills, next_bills_api_url = get_next_oknesset_bills(
            "https://www.oknesset.org{0}".format(next_bills_api_url))
        bills.extend(bills)
    return bills


def get_next_oknesset_bills(bills_url):
    bills_json = json.loads(requests.get(bills_url).text)
    if "objects" in bills_json:
        return bills_json["objects"], bills_json["meta"]["next"]
    return [], None


def get_bill_url(oknesset_bills, bill_name):
    max_ratio = 0.0
    result = ""
    matched_bill = None
    for bill in oknesset_bills:
        ratio = Levenshtein.ratio(strip_stop_words(
            bill["full_title"]), strip_stop_words(bill_name))
        if ratio > max_ratio:
            max_ratio = ratio
            matched_bill = bill
    if matched_bill is not None:
        return "http://www.oknesset.org{0}".format(matched_bill["absolute_url"]), max_ratio, matched_bill["full_title"]
    return None, None


def strip_stop_words(bill_title):
    for word in STOP_WORDS:
        bill_title = bill_title.replace(word, u"")
    return bill_title


def get_commitee_bills_since(since_date=None):
    json_key = json.load(open(CREDENTAIALS_FILE))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key[
                                                'private_key'].encode(), scope)
    spreadsheet = gspread.authorize(
        credentials).open(OCOMMITTEE_SPREADSHEET_NAME)
    worksheet = spreadsheet.worksheet("bills")
    cell_range = "{0}:{1}{2}".format("A2", "B", worksheet.row_count)
    reversed_cells = worksheet.range(cell_range)[::-1]
    matched_cells = []
    for idx, cell in enumerate(reversed_cells):
        if cell.col == MEETING_DATE_COLUMN_INDEX:
            if len(cell.value) > 0:
                bill_date = datetime.datetime.strptime(
                    cell.value, DATE_FORMAT).date()
                if since_date <= bill_date <= datetime.date.today():
                    # Cell in previous column - thus the name column
                    name_cell = reversed_cells[idx - 1]
                    matched_cells.append((name_cell.row, name_cell.value))
    return matched_cells


def get_matched_bills(commitee_bills, oknesset_bills):
    matched_bills = []
    for bill_id, bill_name in commitee_bills:
        url, ratio, oknesset_name = get_bill_url(oknesset_bills, bill_name)
        if url is not None:
            matched_bills.append(Bill(bill_id, bill_name, url, oknesset_name, ratio))
    return matched_bills


def get_execution_api_credentials():
    return json.load(open(EXECUTION_CREDENTIALS_FILE))


def render_bills(bills):
    template_env = Environment(loader=FileSystemLoader(RESOURCES_PATH))
    output_html = template_env.get_template(
        TEMPLATE_FILENAME).render(bills=bills, credentials=get_execution_api_credentials())
    with open(RENDERED_OUTPUT_PATH, "w") as f:
        f.write(output_html.encode("utf8"))


def serve_bills_html(port):
    # Move to commands directory.
    os.chdir(RESOURCES_PATH)
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("localhost", port), Handler)
    threading.Thread(target = lambda: httpd.serve_forever()).start()
    webbrowser.open("http://127.0.0.1:8080/bills.html")


class Command(BaseCommand):
    help = 'Serve an html for manually matching a bill to its url in oknesset.'

    def parse_date(option, opt_str, value, parser):
        try:
            setattr(parser.values, option.dest,
                    datetime.datetime.strptime(value, DATE_FORMAT).date())
        except ValueError:
            return

    option_list = BaseCommand.option_list + (
        make_option('-d', '--date', dest="date",default = datetime.date.today() - datetime.timedelta(weeks = 2), action="callback", type=str, callback=parse_date,
                    help="Show bills for commitee meetings made since this date in format m/d/y. Defaults to two weeks ago."),
        make_option('-p', '--port', nargs='?', default=8080, type=int,
                    help="The port to serve the bills html on. Defaults to 8080")
    )

    def handle(self, *args, **options):
        commitee_bills = get_commitee_bills_since(options['date'])
        if len(commitee_bills) == 0:
            print "No commitee bills available."
            return
        print "There are {0} new commitee bills".format(len(commitee_bills))
        oknesset_bills = get_all_oknesset_bills()
        if len(oknesset_bills) == 0:
            print "No oknesset bills available. perhaps the API is down?"
            return
        print "There are {0} OKnesset bills".format(len(oknesset_bills))
        matched_bills = get_matched_bills(commitee_bills, oknesset_bills)
        render_bills(matched_bills)
        port = options['port']
        print "Serving bills.html on {0}:{1}".format("localhost", port)
        serve_bills_html(port)