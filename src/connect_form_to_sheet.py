from create_executors import executors
from get_access import services

from googleapiclient.errors import HttpError

"""
That was intended to be an automatized process, but
Service Accounts can't deal with Apps Script, so I'm
just leaving it here as a memory
"""

def connect_form_to_sheet():

    services['script'].projects().updateContent(
        scriptId=executors["script"].id,
        body=executors["script"].file
    ).execute()

    request = {
        "function": "linkFormToSpreadsheet"
    }

    try:
        services['script'].scripts().run(scriptId=executors["script"].id, body=request).execute()
        print(f"Form linked to spreadsheet successfully.")
    except HttpError as error:
        print(f"An error occurred while linking form to spreadsheet: {error}")

    print(f"Form URL: {executors["form"].url}")
    print(f"Spreadsheet URL: {executors["spreadsheet"].url}")