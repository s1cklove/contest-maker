from get_access import services
from src.parse_user_data import data

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

import os
from singleton_decorator import singleton

"""
Now, I have to make some routines with access and I decided 
to make it by RAII-wise singleton classes just because
it looks good. Much better than just putting it in a 
direct way.
"""

executors = dict()

@singleton
class Spreadsheet:
    def __init__(self):
        self.body = {
            'properties': {
                'title': data['spreadsheetTitle']
            }
        }
        self.sheet = services['sheets'].spreadsheets().create(
            body=self.body
        ).execute()
        self.id = self.sheet['spreadsheetId']
        self.url = f"https://docs.google.com/spreadsheets/d/{self.id}/edit"
executors["spreadsheet"] = Spreadsheet()

@singleton
class Drive:
    def upload_image(self, path):
        metadata = {'name': os.path.basename(path)}
        media = MediaFileUpload(path)
        image_id = services['drive'].files().create(
            body=metadata,
            media_body=media,
            fields='id'
        ).execute().get('id')
        services['drive'].permissions().create(
            fileId=image_id,
            body={'role': 'reader', 'type': 'anyone'}
        ).execute()
        return f"https://drive.google.com/uc?export=view&id={image_id}"
executors["drive"] = Drive()

@singleton
class Form:
    def __init__(self):
        self.body = {
            "info": {
                "title": data['formTitle'],
            }
        }
        self.form = services['forms'].forms().create(
            body=self.body
        ).execute()
        self.id = self.form['formId']
        self.url = f"https://docs.google.com/forms/d/{self.id}/edit"
executors["form"] = Form()

@singleton
class Permission:
    def __init__(self):
        self.body = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': data['userEmail']
        }
        for executor in ['spreadsheet', 'form']:
            try:
                services['drive'].permissions().create(
                    fileId=executors[executor].id,
                    body=self.body,
                    fields='id'
                ).execute()
            except HttpError:
                print(f"An error occurred while granting access: {HttpError}")
        print(f"Edit access granted to {data['userEmail']}.")
executors["permission"] = Permission()

'''
@singleton
class Script:
    def __init__(self):
        self.body = {
            'title': 'LinkFormToSpreadsheet'
        }
        self.script = services['script'].projects().create(
            body=self.body
        ).execute()
        self.id = self.script['scriptId']
        self.code = f"""
        function linkFormToSpreadsheet() {{
          var form = FormApp.openById('{executors["form"].id}');
          var sheet = SpreadsheetApp.openById('{executors["spreadsheet"].id}');
          form.setDestination(FormApp.DestinationType.SPREADSHEET, sheet.getId());
        }}
        """
        self.file = {
            'files': [{
                'name': 'LinkFormToSpreadsheet',
                'type': 'SERVER_JS',
                'source': executors["script"].code
            }]
        }
executors["script"] = Script()
'''