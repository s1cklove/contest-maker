import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

with open('assets/scopes.json') as f:
    scopes = json.load(f)['links']

credentials = service_account.Credentials.from_service_account_file(
    "oauth.json", scopes=scopes)

services = {
    "forms": build('forms', 'v1', credentials=credentials),
    "drive": build('drive', 'v3', credentials=credentials),
    "sheets": build('sheets', 'v4', credentials=credentials),
    # "script": build('script', 'v1', credentials=credentials)
}
