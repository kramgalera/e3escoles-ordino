# pylint: disable = C0209, R1732, W0718

"Module cointainining utils functions related with Google Cloud usage"

import json
import logging
from google.cloud import storage

def load_json_from_cs (cs_client, bucket_name, file_name):
    """
    Load a JSON file from a Cloud Storage bucket.

    Parameters:
        - cs_client (client): instance of google.cloud.storage.Client
        - bucket_name: name of the Cloud Storage bucket containing the JSON file
        - file_name: name of the JSON file in the Cloud Storage bucket

    Returns:
        - (dict): dictionary containing the parsed JSON data
    """
    bucket = cs_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    file_str = blob.download_as_text()
    file_json = json.loads(file_str)
    return file_json

def download_storage_file (cs_client, bucket_name, file_name, file_dest):
    """
    Downloads a file from Cloud Storage bucket

    Parameters:
        - cs_client (client): instance of google.cloud.storage.Client
        - bucket_name: name of the Cloud Storage bucket containing the JSON file
        - file_name: name of the JSON file in the Cloud Storage bucket
        - file_dest: destination where will be saved the file
    
    Returns:
        - None
    """
    bucket = cs_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    try:
        blob.download_to_filename(file_dest)
        return 'Blob {} downloaded to {}.'.format(file_name, file_dest)
    except NameError:
        return 'File does not exist in bucket {}/{}'.format(bucket_name, file_name)

def _storage_connection (json_auth_path):
    """
    Creates an instance of google.cloud.storage.Client locally

    Parameters:
        - json_auth_path (str): path location of the .json key file
    
    Returns:
        - (client): instance of google.cloud.storage.Client
    """
    return storage.Client.from_service_account_json(json_auth_path)

def insert_data_to_bq (bigquery, schema, data, project_id, bq_dataset, final_table_name):
    """
    Insert dataframe into a BigQuery table.

    Parameters:
        - schema (.json): List of SchemaField objects representing the BQ table schema.
        - data (pd.DataFrame): pandas dataframe containing the csv data.
        - project_id (str): Google Cloud Project ID.
        - bq_dataset (dataset): Name of the BigQuery dataset.
        - final_table_name (str): Name of the BigQuery table to insert into.

    Returns:
        - None {or} (str): number of rows inserted into BQ
    """

    # Initialize BigQuery client
    client = bigquery.Client(project=project_id, credentials=None)

    # Create a LoadJobConfig object to specify the load job settings
    job_config = bigquery.LoadJobConfig()
    job_config.schema = schema
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.autodetect = False  # Since we're providing a schema
    job_config.skip_leading_rows = 0  # To skip the header row

    # Load data into BigQuery
    table_ref = client.dataset(bq_dataset).table(final_table_name.split('.')[-1])
    load_job = client.load_table_from_dataframe(
        data,
        table_ref,
        job_config=job_config,
    )

    try:
        load_job.result()  # Waits for the job to complete and checks for errors
        logging.info("Loaded %s rows to %s", load_job.output_rows, final_table_name)
        return load_job.output_rows

    except Exception as err:
        logging.error("Error occurred while loading data to BigQuery: %s", err)
        return None
