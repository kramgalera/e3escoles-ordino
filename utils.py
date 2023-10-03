# pylint: disable = W0718

'''Module to create utilities functions for the main code'''

import json
from googleapiclient.errors import HttpError

def keep_csv_files (object_list):
    '''
    Removes undesired objects from Google Drive, and keeps only .csv files
    Inputs: list_object (list)
    Output: list_new_object (list)
    '''
    csv_files = [filename for filename in object_list if filename['name'].endswith('.csv')]
    return csv_files

def load_json (file_path):
    """
    Loads json file properly

    Parameters:
        - file_path (str): path of the .json file we want to open
    
    Returns:
        - (.json)
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)

        except BaseException:
            return 'The file contains invalid JSON'

def get_drive_files (client):
    """
    Gets all files from a Drive folder where a GCloud service account has access

    Parameters:
        - client (client): instance of googleapiclient.discovery.build
    
    Returns:
        - files (list): contains all the file names inside the drive folder
    """
    try:
        files = []
        page_token = None
        while True:
            response = client.files().list(
                spaces="drive",
                fields="nextPageToken, files(id, name)",
                pageToken=page_token).execute()
            files.extend(response.get("files", []))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break
    except HttpError as error:
        print(f"An error occurred: {error}")
        files = None
    return files
