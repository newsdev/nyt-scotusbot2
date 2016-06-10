import json
import os
import requests
from sets import Set

from csvkit.py2 import CSVKitDictReader, CSVKitDictWriter


WEBHOOK_URL = os.environ.get('SCOTUSBOT2_WEBHOOK_URL', None)

IMPORTANT = []
with open('important.txt', 'r') as readfile:
    IMPORTANT = list(readfile.read().split(','))

def send_message(message):
    payload = {}
    payload['text'] = message
    payload['icon_url'] = 'https://s3-us-west-2.amazonaws.com/slack-files2/avatars/2014-12-19/3261146648_b3d6178658b2635020f0_48.jpg'
    payload['username'] = "ScotusBot"

    payload_string = json.dumps(payload)
    r = requests.post(WEBHOOK_URL, data=payload_string)

with open('old.csv', 'r') as readfile:
    old_cases = list(CSVKitDictReader(readfile))

with open('new.csv', 'r') as readfile:
    new_cases = list(CSVKitDictReader(readfile))

new_case_ids = Set([x['docket'] for x in new_cases])
old_case_ids = Set([x['docket'] for x in old_cases])

if len(new_cases) > len(old_cases):
    cases = list(new_case_ids.difference(old_case_ids))
    for c in cases:
        for co in new_cases:
            if c == co['docket']:
                message = ''
                if co['docket'] in IMPORTANT:
                    message += ":star: "
                if co['per_curiam'] == 'True':
                    message += "%(docket)s: *%(casename)s*\nPer curiam: <%(opinion_pdf_url)s>\n" % co
                else:
                    message += "%(docket)s: *%(casename)s*\n%(majopinionwriter_name)s: <%(opinion_pdf_url)s>\n" % co
                send_message(message)