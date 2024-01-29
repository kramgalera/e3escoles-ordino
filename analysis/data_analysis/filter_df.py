"""Module dedicated to filter the dataframes"""

import pandas as pd

def filter_by_schedule (dataframe, start_time='08:30:00', end_time='17:00:00'):
    """Description"""

    df = dataframe.copy()
    df['Temperature(°C)'] = df['Temperature(°C)'].apply(lambda x: float(x.replace(',', '.')) if isinstance(x, str) else x)

    mask_time = (df['Time(dd/mm/yyyy)'].dt.strftime('%H:%M:%S') >= start_time) & (df['Time(dd/mm/yyyy)'].dt.strftime('%H:%M:%S') <= end_time)
    df_working_hours = df.loc[mask_time]
    df_working_hours.dropna(axis='rows', how='any', inplace=True)
    df_working_hours.reset_index(inplace=True, drop=True)
    return df_working_hours

def filter_weekend (dataframe):
    """Description"""
    df = dataframe.copy()
    is_weekend = df['Time(dd/mm/yyyy)'].dt.dayofweek >= 5  # 5 and 6 represent Saturday and Sunday
    df = df[~is_weekend]
    df.reset_index(inplace=True, drop=True)
    return df

def filter_vacations (dataframe, vacations):
    """Description"""
    df = dataframe.copy()

    for vacation in vacations:
        list_tmstmp = pd.to_datetime(vacation, format= '%d/%m/%Y %H:%M:%S')
        mask_time = (df['Time(dd/mm/yyyy)'] >= list_tmstmp[0]) & (df['Time(dd/mm/yyyy)'] <= list_tmstmp[1])
        df = df[~mask_time]

    df.reset_index(inplace=True, drop=True)
    #df.drop(columns=['level_0'], inplace=True)
    return df
