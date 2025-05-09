import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Define the scope for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Authenticate and create the Drive API service
def authenticate_google_drive():
    creds = None
    token_path = os.path.join(os.path.dirname(__file__), 'token.pickle')
    credentials_path = os.path.join(os.path.dirname(__file__), r'C:\Users\Raymond\Desktop\DATOS\backend\client_secret_878862563010-eile5ahkijcuildjgr1sig0m8eo67cu2.apps.googleusercontent.com.json')

    # Check if token.pickle exists for saved credentials
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, authenticate the user
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for future use
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

# Upload a file to Google Drive
def upload_to_google_drive(file_path, file_name, file_metadata=None):
    service = authenticate_google_drive()
    if file_metadata is None:
        file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')
