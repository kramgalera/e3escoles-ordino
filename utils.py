'''Module to create easy functions'''

def keep_csv_files (object_list):
    '''
    Removes undesired objects from Google Drive, and keeps only .csv files
    Inputs: list_object (list)
    Output: list_new_object (list)
    '''
    csv_files = [filename for filename in object_list if filename['name'].endswith('.csv')]
    return csv_files