from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import email
from apiclient import errors

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def download_attachments():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    user_id='' 	#Paste your user_id here
    store_dir=""	#Paste your storage directory here



    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    threads = service.users().messages().list(userId=user_id).execute()
    
    for i in range(0,100):
    	msg_id=(threads['messages'][i]['id'])
    	message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    	try:
    		for part in message['payload']['parts']:
    			newvar = part['body']
    			if 'attachmentId' in newvar:
    				att_id = newvar['attachmentId']
    				att = service.users().messages().attachments().get(userId=user_id, messageId=msg_id, id=att_id).execute()
    				data = att['data']
    				file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
    				print(part['filename'])
    				path = ''.join([store_dir, part['filename']])
    				f = open(path, 'wb')
    				f.write(file_data)
    				f.close()
    	except:
    		continue


if __name__ == '__main__':
    download_attachments()