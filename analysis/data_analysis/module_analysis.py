"""Description"""

import pandas as pd

def count_values_survey (dataframe, column_name, column_name_others, tmstmp_column):
    """Description"""
    df = dataframe.copy()

    counts_df = pd.DataFrame(columns=['Value', 'Count'])

    counts = df[column_name].value_counts().reset_index()
    counts.columns = ['Value', 'Count']

    altres_counts = df[df[column_name] == 'other'][column_name_others].value_counts().reset_index()
    altres_counts.columns = ['Value', 'Count']

    counts_df = pd.concat([counts, altres_counts], ignore_index=True)
    counts_df = counts_df.groupby('Value')['Count'].sum().reset_index()
    counts_df['tmstmp'] = counts_df['Value'].apply(lambda x: df[df['he_sentit_fred'] == x][tmstmp_column].tolist())
    return counts_df
