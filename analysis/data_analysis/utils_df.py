# pylint: disable=C0301,W0105

"""Module dedicated to treat the dataframes"""

import json
import pandas as pd

def load_json (file_path):
    """
    Loads json file properly

    Parameters:
        - file_path (str): path of the .json file we want to open
    
    Returns:
        - (.json)
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)

        except BaseException:
            return 'The file contains invalid JSON'

def modify_date (row):
    """shdghd"""
    if row['Time(dd/mm/yyyy)'] >= pd.to_datetime('2024-02-01'):
        return row['Time(dd/mm/yyyy)'].replace(day=row['Time(dd/mm/yyyy)'].month, month=row['Time(dd/mm/yyyy)'].day)
    else:
        return row['Time(dd/mm/yyyy)']
'''# Apply the function to the DataFrame
full_df['Time(dd/mm/yyyy)'] = full_df.apply(modify_date, axis=1)
full_df.sort_values(by='Time(dd/mm/yyyy)', inplace=True)
full_df.reset_index(inplace=True, drop=True)
full_df'''

def add_descriptions (dataframe):
    """Description"""

    full_df = dataframe.copy()
    # Define the Comfort values of the metrics:
    full_df['Temp_Quality'] = ''
    full_df['CO2_Quality'] = ''
    full_df['Humid_Quality'] = ''

    # Temp Quality
    full_df.loc[(full_df['Temperature(°C)'] >= 20.) & (full_df['Temperature(°C)'] <= 26.), 'Temp_Quality'] = 'Confort'
    full_df.loc[full_df['Temperature(°C)'] > 26., 'Temp_Quality'] = 'Calor'
    full_df.loc[full_df['Temperature(°C)'] < 20., 'Temp_Quality'] = 'Fred'

    # CO2 Quality
    full_df.loc[full_df['Carbon dioxide(ppm)'] <= 1000., 'CO2_Quality'] = 'Aire net'
    full_df.loc[(full_df['Carbon dioxide(ppm)'] > 1000.) & (full_df['Carbon dioxide(ppm)'] <= 2000.), 'CO2_Quality'] = "Qualitat baixa de l'aire"
    full_df.loc[(full_df['Carbon dioxide(ppm)'] > 2000.), 'CO2_Quality'] = "Qualitat molt baixa de l'aire"

    # & (full_df['Carbon dioxide(ppm)'] <= 5000.)
    #full_df.loc[(full_df['Carbon dioxide(ppm)'] > 5000.) & (full_df['Carbon dioxide(ppm)'] <= 40000.), 'CO2_Quality'] = 'Critical air quality'
    #full_df.loc[full_df['Carbon dioxide(ppm)'] > 40000., 'CO2_Quality'] = 'Toxic levels for human beings'

    # Humidity Quality
    full_df.loc[full_df['Relative humidity(%)'] < 30., 'Humid_Quality'] = 'Ambient sec'
    full_df.loc[full_df['Relative humidity(%)'] > 50., 'Humid_Quality'] = 'Ambient humit'
    full_df.loc[(full_df['Relative humidity(%)'] >= 30.) & (full_df['Relative humidity(%)'] <= 50.), 'Humid_Quality'] = 'Humitat recomanada'
    return full_df

def references_2023 (dataframe):
    """Description"""

    full_df = dataframe.copy()
    full_df.loc[full_df['Reference'].str.contains('03A48_3rE'), 'Reference'] = full_df['Reference'].str.replace('03A48_3rE', '3rE')
    full_df.loc[full_df['Reference'].str.contains('03A8C_1rD'), 'Reference'] = full_df['Reference'].str.replace('03A8C_1rD', '1rD')
    full_df.loc[full_df['Reference'].str.contains('0E9F5_2nC'), 'Reference'] = full_df['Reference'].str.replace('0E9F5_2nC', '2nC')
    full_df.loc[full_df['Reference'].str.contains('0E8DF_Sem'), 'Reference'] = full_df['Reference'].str.replace('0E8DF_Sem', 'Seminari')
    full_df.loc[full_df['Reference'].str.contains('03A4C_mus'), 'Reference'] = full_df['Reference'].str.replace('03A4C_mus', 'Música')
    full_df.loc[full_df['Reference'].str.contains('03A52_bib'), 'Reference'] = full_df['Reference'].str.replace('03A52_bib', 'Biblioteca')
    full_df.loc[full_df['Reference'].str.contains('03A4E_sal'), 'Reference'] = full_df['Reference'].str.replace('03A4E_sal', 'Sala de Profes')
    full_df.loc[full_df['Reference'].str.contains('03A4D_4tD'), 'Reference'] = full_df['Reference'].str.replace('03A4D_4tD', '4tD')
    full_df.loc[full_df['Reference'].str.contains('0E755_4tB'), 'Reference'] = full_df['Reference'].str.replace('0E755_4tB', '4tB')
    full_df.loc[full_df['Reference'].str.contains('03AAB_1rE'), 'Reference'] = full_df['Reference'].str.replace('03AAB_1rE', '1rE')
    full_df.loc[full_df['Reference'].str.contains('03A49_sem'), 'Reference'] = full_df['Reference'].str.replace('03A49_sem', 'Seminari')
    return full_df

def references_2024 (dataframe):
    """Description"""

    full_df = dataframe.copy()
    full_df.loc[full_df['Reference'].str.contains('03A4C_3rB'), 'Reference'] = full_df['Reference'].str.replace('03A4C_3rB', '3rB_24')
    full_df.loc[full_df['Reference'].str.contains('03A52_2nD'), 'Reference'] = full_df['Reference'].str.replace('03A52_2nD', '2nD_24')
    full_df.loc[full_df['Reference'].str.contains('03A48_4tE'), 'Reference'] = full_df['Reference'].str.replace('03A48_4tE', '4tE_24')
    full_df.loc[full_df['Reference'].str.contains('0E8DF_Sal'), 'Reference'] = full_df['Reference'].str.replace('0E8DF_Sal', 'sala_profes_24')
    full_df.loc[full_df['Reference'].str.contains('03AAB_2nE'), 'Reference'] = full_df['Reference'].str.replace('03AAB_2nE', '2nE_24')
    full_df.loc[full_df['Reference'].str.contains('0E755_1rC'), 'Reference'] = full_df['Reference'].str.replace('0E755_1rC', '1rC_24')
    full_df.loc[full_df['Reference'].str.contains('03A4D_Sem'), 'Reference'] = full_df['Reference'].str.replace('03A4D_Sem', 'seminari_24')
    full_df.loc[full_df['Reference'].str.contains('0E9F5_3rD'), 'Reference'] = full_df['Reference'].str.replace('0E9F5_3rD', '3rD_24')
    full_df.loc[full_df['Reference'].str.contains('03A8C_Bib'), 'Reference'] = full_df['Reference'].str.replace('03A8C_Bib', 'biblioteca_24')
    full_df.loc[full_df['Reference'].str.contains('03A4E_mú'), 'Reference'] = full_df['Reference'].str.replace('03A4E_mú', 'musica_24')
    full_df.loc[full_df['Reference'].str.contains('03A4D_sem'), 'Reference'] = full_df['Reference'].str.replace('03A4D_sem', 'seminari_24')
    full_df.loc[full_df['Reference'].str.contains('03A8C_bib'), 'Reference'] = full_df['Reference'].str.replace('03A8C_bib', 'biblioteca_24')
    full_df.loc[full_df['Reference'].str.contains('03A4E_mus'), 'Reference'] = full_df['Reference'].str.replace('03A4E_mus', 'musica_24')
    full_df.loc[full_df['Reference'].str.contains('0E8DF_sal'), 'Reference'] = full_df['Reference'].str.replace('0E8DF_sal', 'sala_profes_24')
    full_df.loc[full_df['Reference'].str.contains('0E8DF_sal'), 'Reference'] = full_df['Reference'].str.replace('0E8DF_sal', 'sala_profes_24')
    full_df.loc[full_df['Reference'].str.contains('0E8DF_sal'), 'Reference'] = full_df['Reference'].str.replace('0E8DF_sal', 'sala_profes_24')
    full_df.loc[full_df['Reference'].str.contains('0E8DF_sal'), 'Reference'] = full_df['Reference'].str.replace('0E8DF_sal', 'sala_profes_24')
    full_df.loc[full_df['Reference'].str.contains('0E8DF_sal'), 'Reference'] = full_df['Reference'].str.replace('0E8DF_sal', 'sala_profes_24')
    return full_df

def filter_2023_year (dataframe, ini_tmstmp='2022-01-01', fin_tmstmp='2023-09-11'):
    """Description"""
    df = dataframe.copy()
    return df[(df['Time(dd/mm/yyyy)'] >= pd.to_datetime(ini_tmstmp)) & (df['Time(dd/mm/yyyy)'] <= pd.to_datetime(fin_tmstmp))]

def filter_2024_year (dataframe, ini_tmstmp='2023-09-11', fin_tmstmp='2024-06-28'):
    """Description"""
    df = dataframe.copy()
    return df[(df['Time(dd/mm/yyyy)'] >= pd.to_datetime(ini_tmstmp)) & (df['Time(dd/mm/yyyy)'] <= pd.to_datetime(fin_tmstmp))]
