"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


def create_token(secrets_path='../user/google/credentials.json',
                 token_path='../user/google/token.json',
                 scopes='https://www.googleapis.com/auth/spreadsheets.readonly'):
    # Setup the Sheets API
    store = file.Storage(token_path)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(secrets_path, scopes)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    return service


if __name__ == '__main__':
    create_token()
