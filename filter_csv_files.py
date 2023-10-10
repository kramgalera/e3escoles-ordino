"""
One of the main functions filtering the already uploaded .csv files on Cloud Storage
"""

def filter_uploaded_files_files (bq_client, tracker_table_path, csv_files):
    """
    Filters the .csv files from Google Drive, by the ones already uploaded to Cloud Storage

    Parameters:
        - bq_client (Client): instance of google.cloud.Bigquery.Client
        - tracker_table_path (str): Google relative path of the BQ table
        - csv_files (list): contains the names of all .csv files in Drive
    
    Returns:
        - csv_files_def (list): containes the names of the non-uploaded .csv files
    """
    csv_files_def = csv_files.copy()
    # Query `tracker_registry` table in order to obtain new files:
    query = "select file_name, num_lines from  " + tracker_table_path
    query_job = bq_client.query(query)
    rows = query_job.result()
    bq_tracker_results = {}
    bq_tracker_files = []
    for row in rows:
        bq_tracker_results[row.file_name] = [row.num_lines]
        bq_tracker_files.append(row.file_name)

    # Compare both lists and filter already uploaded files
    for file in bq_tracker_files:
        for index, csv in enumerate(csv_files_def):
            if file == csv['name']:
                csv_files_def.pop(index)
    return csv_files_def
