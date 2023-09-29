"Module cointainining utils functions related with Google Cloud usage"

import json

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
    return json.loads(file_str)