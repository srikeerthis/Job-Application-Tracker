from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    cred = None
    if os.path.exists('token.json'):
        cred = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            cred = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(cred.to_json())
    try:
        service = build('gmail', 'v1', credentials=cred)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')

def fetch_emails(service, return_full_message=False):
    try:
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults = 10).execute()
        matching_emails = results.get('messages', [])
        if not matching_emails:
            print('No emails found.')
            return []
        
        if not return_full_message:
            for email in matching_emails:
                msg = service.users().messages().get(userId='me', id=email['id']).execute()
                headers = msg['payload']['headers']
                subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
                print(f'Subject: {subject}')
            return None
        else:
            messages = []
            for email in matching_emails:
                msg = service.users().messages().get(userId='me', id=email['id']).execute()
                messages.append(msg)
            return messages
    except HttpError as error:
        print(f'An error occurred while fetching emails: {error}')
        return []

# if __name__ == '__main__':
#     service = get_gmail_service()
#     if service:
#         print("Gmail service created successfully.")
#         fetch_emails(service=service)
#     else:
#         print("Failed to create Gmail service.")