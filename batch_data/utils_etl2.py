"""
Module to create utilities functions for the main code
"""

import pandas as pd

def refactor_df (df, file_name):
    """
    Refactors the .csv format given by the sensor into the one that will be updated to BQ

    Parameters:
        - df (pd.Dataframe): given dataframe
    
    Returns:
        - dataframe (pd.Dataframe): refactored dataframe
    """

    dataf = df.copy()
    dataf.rename(columns={"Time(dd/mm/yyyy)": 'timestamp', 'Carbon dioxide(ppm)': 'carbon_dioxide', 'Temperature(°C)': 'temperature', 'Relative humidity(%)': 'relative_humidity', 'Atmospheric pressure(hPa)': 'atmospheric_pressure'}, inplace=True)
    dataf.dropna(axis='rows', how='any', inplace=True)
    dataf.reset_index(inplace=True, drop=True)

    # Data types
    dataf['temperature'] = pd.to_numeric(dataf['temperature'].str.replace(',', '.'), errors='coerce')
    dataf['relative_humidity'] = dataf['relative_humidity'].astype(float)
    dataf['carbon_dioxide'] = dataf['carbon_dioxide'].astype(float)

    dataframe = add_parameter_label(dataf, file_name)
    return dataframe

def filter_df (dataframe, file_name, holidays):
    """
    Filters the dataframe removing weekends, holidays, and outside school hours

    Parameters:
        - 
    
    Returns:
        - 
    """
    
    
    return None
def add_parameter_label (df, file_name):
    """
    Adds the category for each parameter of the dataframe

    Parameters:
        - df (pd.Dataframe): given dataframe
    
    Returns:
        - dataframe (pd.Dataframe): refactored dataframe
    """

    dataframe = df.copy()
    dataframe['temperature_label'] = ''
    dataframe['carbon_dioxide_label'] = ''
    dataframe['humidity_label'] = ''
    dataframe['file_name'] = file_name

    # Temperature labeling
    bins_temp = [-float('inf'), 20, 26, float('inf')]
    labels_temp = ['Fred', 'Comfort', 'Calor']
    dataframe['temperature_label'] = pd.cut(dataframe['temperature'], bins=bins_temp, labels=labels_temp)

    # CO2 labeling
    bins_co2 = [-float('inf'), 1000, 2000, 5000, 40000, float('inf')]
    labels_co2 = ['Aire net', "Qualitat baixa de l'aire", "Qualitat molt baixa de l'aire", "Qualitat de l'aire crítica", 'Nivells tòxics per a humans']
    dataframe['carbon_dioxide_label'] = pd.cut(dataframe['carbon_dioxide'], bins=bins_co2, labels=labels_co2)

    # Humidity labeling
    bins_humidty = [-float('inf'), 30, 50, float('inf')]
    labels_humidity = ['Sec', 'Comfort', 'Molt Humit']
    dataframe['humidity_label'] = pd.cut(dataframe['relative_humidity'], bins=bins_humidty, labels=labels_humidity)

    return dataframe
