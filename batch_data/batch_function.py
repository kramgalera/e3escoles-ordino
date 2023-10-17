"""Module containing the function that takes data from Cloud Storage and uploads it to Bigquery"""


def batch_file(bq_client, config, bucket_name, file_path):
    """
    Takes one file from CS and loads its data to BQ
    
    Parameters:
        - bq_client (client): instance of google.cloud.bigquery.Client
        - config (dict): contains all env vars
        - bucket_name (str): name of the Cloud Storage bucket
        - file_path (str): path of the file inserted to BigQuery
    
    Returns:
        - None
    """

    # Load env vars:
    project_id = config['project_id']
    bq_dataset = config['bq_dataset']


    return
