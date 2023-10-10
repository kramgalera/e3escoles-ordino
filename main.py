# pylint: disable= R1732, C0301, W0613, E0611

"""
Main Function of the firt part of the e3escoles project
"""

import os
import datetime
from google.oauth2.service_account import Credentials
from google.cloud import storage
from google.cloud import bigquery
from googleapiclient.discovery import build

from utils import keep_csv_files, get_drive_files
from utils_gcloud import load_json_from_cs, download_storage_file
from upload_files_storage import upload_csv_files_storage
from filter_csv_files import filter_uploaded_files

# Define general env vars:
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'ordino')
CONFIG_FILE_NAME = os.environ.get('CONFIG_FILE_NAME', 'config/config.json')

def storage_to_drive (event):
    """
    Main function checking if new .csv files have been uploaded to GDrive and uploading to CStorage
    """
    # Load config vars + Google Cloud Clients:
    cs_client = storage.Client()
    bq_client = bigquery.Client()
    config = load_json_from_cs(cs_client, BUCKET_NAME, CONFIG_FILE_NAME)

    project_id = config['project_id']
    service_account_file_name = config['service_account_file_name']
    bq_dataset = config['bq_dataset']
    bq_tracker_table = config['bq_tracker_table']

    # Create vars: 
    destination_file = '/tmp/key_file.json'
    tracker_table_path = project_id + '.' + bq_dataset + '.' + bq_tracker_table

    # Build Google Drive Client:
    open(destination_file, 'wt', encoding='utf-8')
    response = download_storage_file(cs_client, BUCKET_NAME, service_account_file_name, destination_file)
    print(response)
    creds = Credentials.from_service_account_file(destination_file)
    drive_client = build('drive', 'v3', credentials=creds)

    # Get Drive .csv file names and filter them:
    files = get_drive_files(drive_client)
    csv_files = keep_csv_files(files)
    csv_files = filter_uploaded_files(bq_client, tracker_table_path, csv_files)

    # Determine year we are at + previous one
    current_year = datetime.datetime.now().year
    previous_year = current_year - 1
    current_year_str = '_' + str(current_year) + '-'
    previous_year_str = '_' + str(previous_year) + '-'

    years = [current_year_str, previous_year_str]
    upload_csv_files_storage(csv_files, drive_client, BUCKET_NAME, tracker_table_path, config, years)
