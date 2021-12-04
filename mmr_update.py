#!/usr/bin/python3

from datetime import date
import os.path
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests

EPIC_NAMES = ('jmlott911', 'Niobiritzu')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1UAyUEHijg-mhKe2NERsrwplbvXrLq8JbQ7I53bSLX3w'


class Sheets(object):

    def __init__(self):
        self.service = None
        self.today = str(date.today())

    def sheet_auth(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('sheets', 'v4', credentials=creds)

    def GetSpreadsheetData(self, sheet, sheet_range):
        time.sleep(1)
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=sheet_range).execute()
        values = result.get('values', [])
        first_empty_row = 0
        row_num = 1
        for row in values:
            row_num += 1

        return row_num

    def WriteSpreadsheetData(self, sheet, name, row_num, data):
        time.sleep(1)
        range_name = name + '!A' + str(row_num) + ':J' + str(row_num)
        today = self.today
        today_list = today.split('-')
        today_date = '%s/%s/%s' % (today_list[1], today_list[2], today_list[0])
        values = self.CreateValues(data, today_date)
        print(values)
        body = {'values': values}
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID, range=range_name,
            valueInputOption='RAW', body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))

    def CreateValues(self, data, today):
        values = [[str(today)]]
        for i in ('Un-Ranked', 'Ranked Duel 1v1', 'Ranked Doubles 2v2', 'Ranked Standard 3v3', 'Rumble', 'Dropshot', 'Hoops', 'Snowday', 'Tournament Matches'):
            try:
                values[0].append(int(data[i]))
            except KeyError:
                values[0].append('100')
        return values


class GCRData(object):

    def __init__(self):
        self.gcr_dict = {}

    def CollectGCRData(self):
        url = 'http://api.yannismate.de/rank/'
        for name in EPIC_NAMES:
            name_url = url + 'epic/' + name
            response = requests.get(name_url)
            data = response.text
            print(data)
            if data.startswith('Player not found'):
                mode_dict = {}
                self.gcr_dict[name] = mode_dict
            else:
                mode_dict = dict((a.strip(), b.strip()) for a, b in (element.split(':') for element in data.split('|')))
                for mode in mode_dict:
                    start = mode_dict[mode].find('(')
                    end = mode_dict[mode].find(')')
                    if start != -1 and end != -1:
                        mode_dict[mode] = int(mode_dict[mode][start+1:end])
            self.gcr_dict[name] = mode_dict
        print('MMR data collected...')


def main():
    sheets = Sheets()
    sheets.sheet_auth()
    sheet = sheets.service.spreadsheets()
    gcr = GCRData()
    gcr.CollectGCRData() 
    data = gcr.gcr_dict
    #print(data)
    for name in EPIC_NAMES:
        sheet_range = name + '!A1:J500'
        row_num = sheets.GetSpreadsheetData(sheet, sheet_range)
        sheets.WriteSpreadsheetData(sheet, name, row_num, data[name])



if __name__ == '__main__':
    main()
