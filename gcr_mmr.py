#!/usr/bin/python3

from datetime import date
import os.path
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests

EPIC_NAMES = ('crippledw0ffle', 'OriCakes', 'Seraphiim.', 'Heli12345', 'stevyjoe', 'ryanjr123', 'Canyongrand', 'Lced Chai Latte',
              'OTG_Natsu', 'JDiddlezz', 'ElfOnAShelfNA', 'shorterchild', 'MiSFITsk8s', 'Nigel Thornbrake', 'Dasiago_', 'cloudwrath_11',
              'Steelrain13f', 'jmlott911', 'Gypsy Cats', 'ShaggyLemur783', 'Jaydoom244', 'SshadowWSsponsS', 'Vytarien', 'Viroscope',
              'westcoastdogos', 'chefwesty96', 'Infantryboyz09', 'Ballchasin Bill', 'Niobiritzu', 'Kaptajn Kødpølse', 'Nitrate_TTV',
              'Chaabraa', 'UnseenGhost', 'Whoo0oosh', 'hazardezhemp', 'dead_guy66613777', 'Dabod.', 'Typhol.', 'zoivibi3', 'oTp Nova',
              'Alex_Brave', 'SemanticSwan853', 'Minus_rc', 'audiolovin', 'CrustyMustard', 'KomaliBear', 'MeRLiN_FTW.', 'arterialice',
              'notori0us sn0w', 'Dulkalicious', 'MCRD-', 'EnVy', 'fasterthanfalcon', 'zamyti', 'Nycto_Jedi', 'PhantomGames6',
              'IsaacGarcia94', 'lostmymindd779', 'RL.BirdPlayz', 'Daffy Duckz', 'TyrannusRex499', 'Tornado Master', 'GirlyNinja_XP',
              'EddieTheEd', 'Lifeblood_', 'Sk3ptixx', 'J.G.Pageau', 'IHateArmpits', 'oleuglyboii', 'BlueLiger739', 'AgentSmith310',
              'Krypt Kirito', 'Suduko20', 'uvBlur', '7th Raiju', 'EuRoThOr', 'Deliiriousss', 'YokyRLM', 'DiirtyGymSock', 'TFDoe2',
              'eZ Stylzzz', 'Kingpeter90999', 'MeWeeney', 'merlinsmaster', 'KAMGFXA', 'CrazySwede962', 'dog123idk', 'Deltons Peaking',
              'LowPumpkin118', 'RogueAce47', 'Unleash IG', 'OurMutualFiend', 'Icy .J.', 'Ninji.XIX', 'ANTEG0', 'ginny3224', 'revault9195',
              'Platzel')
STEAM_NAMES = {'CrustyMustard' : '76561198035518215', 'merlinsmaster': '76561198074247056', 'KAMGFXA': '76561197960555095',
               'EnVy': '76561197980005984'}
XBL_NAMES = {'EuRoThOr': 'eurothor', 'MeWeeney': 'Me Weeney'}
SHEET_MAP = {'crippledw0ffle': 'DommyBoi', 'Seraphiim.': 'jimmydean', 'ryanjr123': 'JR', 'Canyongrand': 'GrandCanyon',
             'Lced Chai Latte': 'IcedChaiLatte', 'OTG_Natsu': 'Natsu', 'ElfOnAShelfNA': 'ElfOnAShelf', 'shorterchild': 'RichE',
             'MiSFITsk8s': 'MISFITsk8s', 'Dasiago_': 'Dasiago', 'cloudwrath_11': 'cloudwrath11', 'ShaggyLemur783': 'Niky',
             'Jaydoom244': 'Jaydoom', 'SshadowWSsponsS': 'ShadowSpons', 'Whoo0oosh': 'So Hypnotics', 'dead_guy66613777': 'deadguy',
             'Dabod.': 'Dabod', 'Typhol.': 'OG SauceMane', 'zoivibi3': 'z0mbi3', 'oTp Nova': 'Cloud (Seth)', 'Alex_Brave': 'Bravo',
             'SemanticSwan853': 'pHaTe', 'Minus_rc': 'Minus', 'CrustyMustard': 'Janky Ape', 'MeRLiN_FTW.': 'MeRLiNftw',
             'arterialice': 'iceberg', 'notori0us sn0w': 'notori0ussn0w', 'zamyti': 'Zamyti', 'Nycto_Jedi': 'Nycto',
             'PhantomGames6': 'PhantomGames', 'IsaacGarcia94': 'IsaacGarcia', 'lostmymindd779': 'lostmymind', 'TyrannusRex499': 'Rex',
             'Tornado Master': 'MeleeStyx', 'GirlyNinja_XP': 'GirlyNinja', 'EddieTheEd': 'Stry', 'Lifeblood_': 'SlopClam',
             'J.G.Pageau': 'vegie1999', 'IHateArmpits': 'G00lash', 'oleuglyboii': 'Coty Colorado', 'BlueLiger739': 'Crazy Coal Train',
             'AgentSmith310': 'Agentsmith310', 'Suduko20': 'Suduko', '7th Raiju': 'Raiju', 'Deliiriousss': 'Deliriouss',
             'YokyRLM': 'Yoky', 'DiirtyGymSock': 'DirtyGymSock', 'TFDoe2': 'TF Doe', 'eZ Stylzzz': 'eZSloth', 'Kingpeter90999': 'KingpeterM8',
             'CrazySwede962': 'CrazySwede', 'dog123idk': 'emon', 'Deltons Peaking': 'Delton', 'LowPumpkin118': 'nova', 'RogueAce47': 'RogueAce',
             'Icy .J.': 'Spicy J', 'Ninji.XIX': 'Ninji', 'ANTEG0': 'Antego', 'ginny3224': 'Ginny', 'revault9195': 'revault'}

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1kUcZfdQweLdRDF2uXBipMEGAagz2pNqFSEROjyH0JqI'


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
            if row == []:
                first_empty_row = row_num
                break
            row_num += 1

        return first_empty_row

    def WriteSpreadsheetData(self, sheet, name, row_num, data):
        time.sleep(1)
        range_name = name + '!A' + str(row_num) + ':M'
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
        values = [[today]]
        for i in ('Un-Ranked', 'Ranked Duel 1v1', 'Ranked Doubles 2v2', 'Ranked Standard 3v3', 'Rumble', 'Dropshot', 'Hoops', 'Snowday', 'Tournament Matches'):
            try:
                values[0].append(data[i])
            except KeyError:
                values[0].append('100')
        return values


class GCRData(object):

    def __init__(self):
        self.gcr_dict = {}

    def CollectGCRData(self):
        url = 'http://api.yannismate.de/rank/'
        for name in EPIC_NAMES:
            name_url = None
            if name in STEAM_NAMES:
                new_name = STEAM_NAMES[name]
                platform = 'steam'
                name_url = url + platform + '/' + new_name
            elif name in XBL_NAMES:
                new_name = XBL_NAMES[name]
                platform = 'xbox'
                name_url = url + platform + '/' + new_name
            else:
                name_url = url + 'epic/' + name
            response = requests.get(name_url)
            data = response.text
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
        new_name = None
        try:
            new_name = SHEET_MAP[name]
        except KeyError:
            new_name = name
        sheet_range = new_name + '!A1:M73'
        row_num = sheets.GetSpreadsheetData(sheet, sheet_range)
        sheets.WriteSpreadsheetData(sheet, new_name, row_num, data[name])



if __name__ == '__main__':
    main()
