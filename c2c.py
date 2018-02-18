# -*- coding: utf-8 -*-

#
# A ical file generator based on connpass events.
# 
# Preparations:
#   $ pip install icalendar dateutil
# Usage:
#   $ python c2c.py <keywords> > <filename>
# Example:
#   $ python c2c.py php,ruby,python > llstudy.ics
#

from dateutil import parser
from icalendar import Calendar, Event
import os
import requests
import sys
import tempfile

# Max results = 100 is server side upper limit.
CONNPASS_SEARCH_API = 'https://connpass.com/api/v1/event/?count=100&keyword_or='
TMPFILE = 'temp.ics'
PRODID = '-//syucream connpass calendar//connpass2cal//'

def _get_connpass_events(keyword):
    res = requests.get(CONNPASS_SEARCH_API + keyword)
    return res.json()['events']

def _generate_ical(events):
    ical = Calendar()
    ical.add('version', '2.0')
    ical.add('prodid', PRODID)

    for e in events:
        iev = Event()
        iev.add('summary', e['title'])
        iev.add('description', 'Event URL: ' + e['event_url'] + '\n\n' + e['description'])
        iev.add('dtstart', parser.parse(e['started_at']))
        iev.add('dtend', parser.parse(e['ended_at']))
        ical.add_component(iev)

    return ical.to_ical()

def _dump_via_tmpfile(ical):
    directory = tempfile.mkdtemp()

    wf = open(os.path.join(directory, TMPFILE), 'wb')
    wf.write(ical)
    wf.close()

    rf = open(os.path.join(directory, TMPFILE), 'r')
    data = rf.read()
    rf.close()

    return data

if __name__ == '__main__':
    keywords = sys.argv[1]
    events = _get_connpass_events(keywords)
    ical = _generate_ical(events)
    out = _dump_via_tmpfile(ical)
    print(out)
