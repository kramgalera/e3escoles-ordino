"""Hello World"""

import os
import pandas as pd

def convert_time_scale (input_df):
    """
    Converts a 5min scale timestamp into a 10min scale.

    Parameters:
        - df_5min (datfaframe): 5-minutal dataframe
    
    Output:
        - df (dataframe)    
    """

    df = input_df.copy()
    df['Temperature(°C)'] = df['Temperature(°C)'].str.replace(',', '.')
    df['Temperature(°C)'] = pd.to_numeric(df['Temperature(°C)'])

    #We convert the 5 minutal data into 10 minutal, by making a mean bewteen consecutive measures:
    max_len = len(df)-1
    for index, value in enumerate(df['Time(dd/mm/yyyy)']):
        if not index % 2 == 0:
            if index < max_len:
                df.at[index+1, 'Carbon dioxide(ppm)'] = (df['Carbon dioxide(ppm)'].iloc[index] + df['Carbon dioxide(ppm)'].iloc[index+1])/2
                df.at[index+1, 'Temperature(°C)'] = (df['Temperature(°C)'].iloc[index] + df['Temperature(°C)'].iloc[index+1])/2
                df.at[index+1, 'Atmospheric pressure(hPa)'] = (df['Atmospheric pressure(hPa)'].iloc[index] + df['Atmospheric pressure(hPa)'].iloc[index+1])/2
                df.at[index+1, 'Relative humidity(%)'] = (df['Relative humidity(%)'].iloc[index] + df['Relative humidity(%)'].iloc[index+1])/2

    #We reloop the df in a separate loop, due to the problems of the new length when deleting rows
    new_max_len = len(df)-1
    for index, value in enumerate(df['Time(dd/mm/yyyy)']):
        if not index % 2 == 0:
            if index < new_max_len:
                df.drop(index, inplace=True)

    df.reset_index(inplace=True)
    df.drop(columns=['index'])
    return df

# Get current folder path:
print(os.getcwd())

# Load df:
df_5min = pd.read_csv('./Data/10_24/0E9F5_2nC_2022-10-24T13_19_18+0200.csv')
df_10min = convert_time_scale(df_5min) 
df_10min.to_csv('./Data/10_24/0E9F5_2nC_2022-10-24.csv', index=False)
