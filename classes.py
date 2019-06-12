import os
import time
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import request_dict


def find_str(test_str, str_to_find):
    counter = 0
    for i in test_str:
        if i == str_to_find:
            counter += 1
    return counter


def even(number):
    return number % 2 == 0 and number != 0


class Document:
  
    def __init__(self, ID, scope):
        self.ID = ID
        self.scope = scope
        self.data = None

    def on_change(self, timeout=-1):
        # this returns the current document once it is changed
        # if the timeout is exceded then it rases an error
        past = self.get()
        while timeout != 0:
            for i in range(10):
                current = self.get()
                if past != current:
                    self.data = current
                    return current
                time.sleep(0.1)
            timeout -= 1
        raise TimeoutError

    @staticmethod
    def find_backs(string, look_for):
        first = string.find(look_for) + 1
        second = string.find(look_for, first+1)
        return first, second

    def find_backticks(self):
        # returns an nested list of the location of backticks
        # format [[startIndex, endIndex], ...]
        index_list = []
        for i in self.data.get('body').get('content'):
            try:
                content = i.get('paragraph').get('elements')[0].get('textRun').get('content')
                if content is not None:
                    if even(find_str(i.get('paragraph').get('elements')[0].get('textRun').get('content'), '`')):
                        first, second = Document.find_backs(i.get('paragraph').get('elements')[0].get('textRun').get('content'), '`')
                        startIndex = i.get('startIndex') + first
                        endIndex = i.get('startIndex') + second
                        index_list.append([startIndex, endIndex])
            except AttributeError:
                continue
        return index_list

    @staticmethod
    def get_sample_request(check=False):
        if check:
            return
        return request_dict.sample_request

    def add_code_blocks(self, locations):
        requests = {}
        for startIndex, endIndex in locations:
            request = self.get_sample_request()
            request.get('range').update({'startIndex': startIndex})
            request.get('range').update({'endIndex': endIndex})
            requests.update({"updateTextStyle": request})
            result = service.documents().batchUpdate(documentId=self.ID, body={'requests': requests}).execute()
        service.documents().batchUpdate(documentId=self.ID, body={'requests': {'replaceAllText': request_dict.delete_backs}}).execute()
        return result

    def get(self):
        global service
        DOCUMENT_ID = self.ID
        SCOPES = self.scope
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
        self.data = document
        return document
