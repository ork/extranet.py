import requests
import json
import re
from datetime import date, datetime, timedelta
from extranet.exceptions import *

UA_STRING = 'Mozilla/5.0 (Extranet-py)'

LOGIN_URL = '/Users/Account/DoLogin'
EVENT_URL = '/Student/Calendar/GetStudentEvents'
DOCUMENTS_TREE_URL = '/Student/Home/GetDocumentTree'
DOCUMENTS_URL = '/Student/Home/GetDocuments'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

TITLE_FORMAT = r'(?P<title>.*)\s+-\s+(?P<teacher>.*)\s+-\s+(?P<room>.*)\s+$'
BADJSON_FORMAT = r'X\.net\.RM\.getIcon\("\w+"\)'

def extranet_event_parser(dct):
    # Parse date and time
    for k, v in dct.items():
        if k in ['start', 'end']:
            try:
                dct[k] = datetime.strptime(v, DATE_FORMAT)
            except:
                pass

    # Parse title and extract title, teacher and room
    parsed_title = re.search(TITLE_FORMAT, dct['title']).groupdict()
    dct.update(parsed_title)

    return dct

class Extranet(object):

    def __init__(self, base_url=None, username=None, password=None):
        self._username = username
        self._password = password

        self.base_url = base_url
        self.connected = False
        self.logged = False
        self.session = None

    def init_connection(self):
        if not self.session:
            self.session = requests.Session()

        self.session.headers.update({'User-Agent': UA_STRING})

        try:
            self.session.get(self.base_url)
        except requests.ConnectionError as e:
            raise ConnectionError
        else:
            if not 'ASP.NET_SessionId' in self.session.cookies:
                raise FatalError
            else:
                self.connected = True

    def login(self):
        if not self.connected:
            self.init_connection()

        auth_info = {
            'username': self._username,
            'password': self._password
        }

        self.session.post(self.base_url + LOGIN_URL, params=auth_info)

        if not 'extranet_db' in self.session.cookies:
            raise LoginError
        else:
            self.logged = True

    def get_timetable(self, start, end):
        if not self.logged:
            self.login()

        timetable_delta = {
            'start': start.timestamp(),
            'end': end.timestamp()
        }

        r = self.session.get(self.base_url + EVENT_URL, params=timetable_delta)

        return json.loads(r.text, object_hook=extranet_event_parser)

    def get_planning(self, start=None, weeks=3):
        if start is None:
            # Default, begin monday of the current week
            today = datetime.combine(date.today(), datetime.min.time())
            last_monday = today - timedelta(days=today.weekday())
            start = last_monday

        next_weeks = start + timedelta(weeks=weeks)

        return self.get_timetable(start, next_weeks)

    def get_documents_categories(self):
        if not self.logged:
            self.login()

        r = e.session.get(self.base_url + DOCUMENTS_TREE_URL)
        good_json = re.sub(BADJSON_FORMAT, '"osef"', r.text)

        parsed_json = json.loads(good_json)

        categories = {}
        for cat in parsed_json['children']:
            categories[cat['id']] = cat['text']

        return categories

    def get_documents(self):
        categories = self.get_documents_categories()

        for cat, title in categories.items():
            paging = {
                'document_type' : cat,
                'page' : 1,
                'start' : 0,
                'limit' : 25,
            }

            r = e.session.get(self.base_url + DOCUMENTS_URL, params=paging)

            parsed_json = json.loads(r.text)

