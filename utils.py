# pylint: disable = W0718

'''Module to create utilities functions for the main code'''

import json
import io
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

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

def download_file_from_drive (drive_client, file_id, file_path):
    """
    Downloads file from Google Drive

    Parameters:
        - drive_client (client): instance of googleapiclient.discovery.Resource
        - file_id (str): id of the file that has to be downloaded
        - file_name (str): path where the file will be saved
    
    Returns:
        - (str): result message
    """
    request = drive_client.files().get_media(fileId=file_id)
    local_file = io.FileIO(file_path, 'wb')
    downloader = MediaIoBaseDownload(local_file, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%")

def find_index_of_substring(string, substring):
    """
    Gives index position of the substring in the string

    Parameters:
        - string (str): long string containing substring
        - substring (str): substring that we want to locate
    
    Returns:
        - index (int): position where is located the substring inside the string
    """
    index = string.find(substring)
    return index

def blob_to_filename(blob_list):
    """
    Takes a list containing blobs and retrieves its name

    Parameters:
        - blob_list (list): contains several instances google.cloud.storage.blob.Blob
    
    Returns:
        - folders (list): contains the name for each blob
    """
    folders = []
    for blob in blob_list:
        if blob.name.endswith('/'):
            if blob.name != 'data/':
                folders.append(blob.name[5:-1])
    return folders
