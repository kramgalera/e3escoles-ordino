
"Module cointainining utils functions related with Google Cloud usage"

import json
from google.cloud import storage, bigquery

def load_json_from_cs (cs_client, bucket_name, file_name):
    """
    Load a JSON file from a Cloud Storage bucket.

    Parameters:
        - cs_client (client): instance of google.cloud.storage.Client
        - bucket_name (str): name of the Cloud Storage bucket containing the JSON file
        - file_name (str): name of the JSON file in the Cloud Storage bucket

    Returns:
        - (dict): dictionary containing the parsed JSON data
    """
    bucket = cs_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    file_str = blob.download_as_text()
    file_json = json.loads(file_str)
    return file_json

def _bigquery_connection (json_auth_path):
    """
    Creates an instance of google.cloud.storage.Client locally

    Parameters:
        - json_auth_path (str): path location of the .json key file
    
    Returns:
        - (client): instance of google.cloud.storage.Client
    """
    return bigquery.Client.from_service_account_json(json_auth_path)

def _storage_connection (json_auth_path):
    """
    Creates an instance of google.cloud.storage.Client locally

    Parameters:
        - json_auth_path (str): path location of the .json key file
    
    Returns:
        - (client): instance of google.cloud.storage.Client
    """
    return storage.Client.from_service_account_json(json_auth_path)