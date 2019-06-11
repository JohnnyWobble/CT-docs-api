from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import classes


updateTestStyle_request = {
  'updateTextStyle': {
    'range': {
      'segmentId': None,
      'startIndex': None,
      'endIndex': None
    },
    'textStyle': {
      "foregroundColor": {
        'color': {
          'rgbColor': {
            'red': 0.2,
            'green': 0.2,
            'blue': 0.2
          }
        }
      },
      "backgroundColor": {
        'color': {
          'rgbColor': {
            'red': 0.96,
            'green': 0.96,
            'blue': 0.96
          }
        }
      },
      "fontSize": {
        'magnitude': 10,
        'unit': 'PT'
      },
      "weightedFontFamily": {
        'fontFamily': 'Courier New',
        'weight': 400
      },
    },
    'fields': 'backgroundColor, foregroundColor, fontSize, weightedFontFamily'
  }
}


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
DOCUMENT_ID = '1UeorM9adOh8Nds1Z457RRKBZMkh0VZ_kn_jllpkzh7U'
service = None


def setup():
    global service
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID).execute()
    return document


def edit_testStyle_request(startIndex=None, endIndex=None):
    updateTestStyle_request.get('updateTextStyle').get('range').update({'startIndex': startIndex})
    updateTestStyle_request.get('updateTextStyle').get('range').update({'endIndex': endIndex})
    wb = updateTestStyle_request.get('updateTextStyle').get('range')
    print(wb)
    return updateTestStyle_request


# def edit_updateText


def update(request):
    result = service.documents().batchUpdate(
        documentId=DOCUMENT_ID, body={'requests': request}).execute(num_retries=10)
    return result

