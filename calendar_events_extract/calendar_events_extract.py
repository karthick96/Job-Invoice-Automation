from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pandas as pd

# date time related packages
import datetime


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def calendar_events_extract(start_date=None, end_date=None, path='calendar_events_extract', filter_desc=None, filtered_calendars=None, maxResults=1000):
    """Extract all the filtered events for the provided window using the Google Calendar API.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_json_path = os.path.join(path, 'token.json')
    if os.path.exists(token_json_path):
        creds = Credentials.from_authorized_user_file(token_json_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except:
                os.remove(token_json_path)
                return 0
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(path, 'credentials.json'), SCOPES)
            creds = flow.run_local_server(port=8080)  # 0
        # Save the credentials for the next run
        with open(token_json_path, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

        # Iterate through entries in calendar list
        available_calendars = {}
        page_token = None
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                # id and name of the available calendars
                available_calendars[calendar_list_entry['id']
                                    ] = calendar_list_entry['summary']
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

        # print(available_calendars)

        # get all the events from available calendars
        events = []
        for calendar_id,  calendar_name in available_calendars.items():
            if filtered_calendars is None:
                events_result = service.events().list(calendarId=calendar_id,
                                                      timeMin=start_date,
                                                      timeMax=end_date,
                                                      maxResults=maxResults,
                                                      singleEvents=True,
                                                      orderBy='startTime'
                                                      ).execute()
                events.extend(events_result.get('items', []))
            elif calendar_name in filtered_calendars:
                events_result = service.events().list(calendarId=calendar_id,
                                                      timeMin=start_date,
                                                      timeMax=end_date,
                                                      maxResults=maxResults,
                                                      singleEvents=True,
                                                      orderBy='startTime'
                                                      ).execute()

                events.extend(events_result.get('items', []))
        print(type(events))

        # if no events found return
        if not events:
            print('No upcoming events found.')
            return 0

        # Extract and output the events info in a dataframe
        columns = ['event_start_dtm', 'event_end_dtm',
                   'event_description', 'event_hours']
        output_df = pd.DataFrame(columns=columns)
        date_format = '%m/%d/%Y %I:%M%p'
        row_num = 0
        for event in events:
            if 'summary' in event:
                if filter_desc is None or filter_desc in event['summary']:
                    start = event['start'].get(
                        'dateTime', event['start'].get('date'))
                    end = event['end'].get(
                        'dateTime', event['end'].get('date'))

                    start = datetime.datetime.strftime(datetime.datetime.strptime(
                        start[:-6], "%Y-%m-%dT%H:%M:%S"), date_format)

                    end = datetime.datetime.strftime(datetime.datetime.strptime(
                        end[:-6], "%Y-%m-%dT%H:%M:%S"), date_format)

                    diff = int(end[-7:-5])-int(start[-7:-5])

                    output_df.loc[row_num, 'event_start_dtm'] = start
                    output_df.loc[row_num, 'event_end_dtm'] = end
                    output_df.loc[row_num,
                                  'event_description'] = event['summary']
                    output_df.loc[row_num, 'event_hours'] = str(diff).split(':')[
                        0]

                    # print(str(start)+','+str(end)+',' +
                    #     event['summary']+','+str(diff).split(':')[0])

                    row_num += 1
        return output_df

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    out = calendar_events_extract(filter_desc='class',
                                  filtered_calendars=[
                                      'My Schedule', 'karthickrajamrita@gmail.com'],
                                  # start_date=datetime.datetime(
                                  #   2022, 6, 1, 00, 00, 00, 0).isoformat() + 'Z',
                                  # end_date=datetime.datetime(
                                  #   2022, 7, 1, 00, 00, 00, 0).isoformat() + 'Z'
                                  )
    if isinstance(out, pd.DataFrame):
        print(out)
    else:
        print(
            "refresh token expired! so, deleting token.json and requesting access again!!!")
        print(
            calendar_events_extract(filter_desc='class',
                                    filtered_calendars=[
                                        'My Schedule', 'karthickrajamrita@gmail.com'],
                                    # start_date=datetime.datetime(
                                    #   2022, 6, 1, 00, 00, 00, 0).isoformat() + 'Z',
                                    # end_date=datetime.datetime(
                                    #   2022, 7, 1, 00, 00, 00, 0).isoformat() + 'Z'
                                    )
        )
