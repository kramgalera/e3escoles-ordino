'''This script is dedicated to establish the connection with the GoogleCloud Servers, and make basic manipulations in BigQuery'''

import os
from google.cloud import bigquery as bq
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()
JSON_AUTH_PATH = os.getenv('gcloud_json_key')

def big_query_conn (JSON_AUTH_PATH):
    '''{{add desctiption}}'''
    return bq.Client.from_service_account_json(JSON_AUTH_PATH)

def storage_connection (JSON_AUTH_PATH):
    '''{{add desctiption}}'''
    return storage.Client.from_service_account_json(JSON_AUTH_PATH)

def job_configuration_insert():
    job_config = bq.LoadJobConfig()
    job_config.write_disposition = 'WRITE_TRUNCATE'
    job_config.autodetect = True
    job_config.ignore_unknown_values = True

def remove_duplicates(client, table_id, column):
    # Query to remove duplicates
    query_rm_dupl = f'''
        create or replace table `{table_id}` as (
        select * except(row_num) from (
            select *,
                row_number() over ( partition by {column} order by {column} ) row_num
            from
            {table_id}) t
        where row_num=1
        )
    '''
    # Run the query
    #job_config = bq.QueryJobConfig()
    query_job = client.query(query_rm_dupl)
    rows = query_job.result()

    return 'Duplicates removed successfully', rows