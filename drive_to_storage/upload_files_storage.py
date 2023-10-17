# pylint: disable = C0301, W0612

"""
One of the main functions uploading the filtered .csv files to Cloud Storage and storing a registry of the file in a BQ table
"""
import datetime
from google.cloud import storage, bigquery

from utils import find_index_of_substring, download_file_from_drive, count_csv_length
from utils_gcloud import upload_storage_file, insert_row_to_bq

def upload_csv_files_storage (csv_files, drive_client, bucket_name, tracker_table_path, config, year):
    """
    Uploads each .csv file to Cloud Storage and updates the `tracker_registry` table

    Parameters:
        - csv_files (list): list of dicts containing the names and id of the new .csv files
        - drive_client (Client): instance of googleapiclient.discovery.build
        - bucket_name (str): name of the Cloud Storage bucket containing the JSON file
        - tracker_table_path (str): Google relative path of the BQ table
        - config (dict): contains all env vars
        - year (list): contains present and past year in str format
    
    Returns:
        - None
    """

    # Load vars and Google Clients
    cs_client = storage.Client()
    bq_client = bigquery.Client()

    data_blob = config['storage_blobs']['data_blob']
    tracker_table_headers = config['tracker_table_headers']

    current_year_str = year[0]
    previous_year_str = year[1]

    # Main script for each file:
    for index, file in enumerate(csv_files):
        # Calculate index of our substring:
        index_string = find_index_of_substring(file['name'], current_year_str)
        if index_string == -1:
            index_string = find_index_of_substring(file['name'], previous_year_str)

        # Extract date of the file
        date_file = file['name'][index_string+1:index_string+11]

        # Download file from Drive:
        local_file_path = '/tmp/' + file['name']
        download_file_from_drive(drive_client, file['id'], local_file_path)

        # Count rows of csv file:
        len_file = count_csv_length(local_file_path)
        current_tmstmp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        #if date_file in tmstmp_folders:
        storage_blob_path = data_blob + date_file + '/' + file['name']
        response = upload_storage_file(cs_client, bucket_name, storage_blob_path, local_file_path)

        if response == "Upload done succesfully":
            tracker_data = [file['name'], len_file, 0, current_tmstmp]
            row_data = dict(zip(tracker_table_headers, tracker_data))
            insert_row_to_bq(client=bq_client, table_id= tracker_table_path, row=row_data)
