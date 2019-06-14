import datetime
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
TWSC_CALENDAR = '59o7f5ng87g2ilq635r5r78o04@group.calendar.google.com'
WEEK_DELTA = datetime.timedelta(days=7)
WEEK_STR = "一二三四五六日"
CRED_PATH = './config/credentials.json'
TOKEN_PATH = './config/token.pickle'


class TwscCalendar:
    def __init__(self):
        self.creds = self.get_creds()

    def get_creds(self):
        creds = None
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CRED_PATH, SCOPES)
                creds = flow.run_local_server()
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def _get_utcstr(self, t):
        return t.strftime('%Y-%m-%dT00:00:00Z')

    def _get_time(self):
        now = datetime.datetime.now()
        end = now + WEEK_DELTA

        now = self._get_utcstr(now)
        end = self._get_utcstr(end)

        return now, end

    def get_events(self, max_result=50):
        service = build('calendar', 'v3', credentials=self.creds)

        now, end = self._get_time()

        events_result = service.events().list(  # pylint: disable=no-member
            calendarId=TWSC_CALENDAR, maxResults=max_result, singleEvents=True,
            timeMin=now, timeMax=end, orderBy='startTime').execute()
        events = events_result.get('items', [])

        return events

    def parse_event(self, e):
        title = e['summary'].replace('[SC2] ', '')
        date = e['start'].get('dateTime', e['start'].get('date'))
        date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+08:00')

        return '%s (%s) %s %s' % (
            date.strftime('%m/%d'),
            WEEK_STR[date.weekday()],
            date.strftime('%H:%M'), title
        )

    def get_recent_events(self):
        return '\n'.join([self.parse_event(e) for e in self.get_events()])


if __name__ == '__main__':
    tc = TwscCalendar()
    print(tc.get_recent_events())
