"""

"""

import os
import logging
from google.cloud import storage, bigquery

from utils_module import load_json_from_cs
from batch_function_module import batch_file

BUCKET_NAME = os.environ.get('BUCKET_NAME', 'ordino')
CONFIG_FILE_NAME = os.environ.get('CONFIG_FILE_NAME', 'config/config.json')

def batch_main (event):
    """
    Entry point for streaming function calls from Cloud Storage triggers
    
    Parameters:
        - event (cs_event): event triggered by Cloud Storage
    
    Returns:
        - None
    """

    file_path = event['name']

    # Load the credentials json file
    cs_client = storage.Client()
    bq_client = bigquery.Client()

    if file_path.slipt[0] == 'data':
        config = load_json_from_cs(cs_client, BUCKET_NAME, CONFIG_FILE_NAME)
        batch_file(bq_client, config, BUCKET_NAME, file_path)
    else:
        logging.warning("CloudFunction is triggered, but exited as the source file is from '%s' and not from 'data/' folder", file_path.split[0])
