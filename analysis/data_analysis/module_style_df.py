import pandas as pd

def style_cell_co2 (value):
    limit1 = 400; limit2 = 1000; limit3 = 2000; limit4 = 5000; limit5 = 40000
    if value <= limit1:
        return 'background-color: green; color: black'
    elif (value > limit1) & (value <= limit2):
        return 'background-color: lightgreen; color: black'
    elif(value > limit2) & (value <= limit3):
        return 'background-color: yellow; color: black'
    elif(value > limit3) & (value <= limit4):
        return 'background-color: orange; color: black'
    elif(value > limit4) & (value <= limit5):
        return 'background-color: red; color: black'
    elif value > limit5:
        return 'background-color: darkred; color: black'
    elif pd.isna(value):
        return 'background-color: white; color: red'

def style_cell_temp (value):
    limit1 = 20; limit2 = 26
    if value < limit1:
        return 'background-color: lightblue; color: black'
    elif (value >= limit1) & (value <= limit2):
        return 'background-color: lightgreen; color: black'
    elif (value > limit2):
        return 'background-color: red; color: black'
    elif pd.isna(value):
        return 'background-color: white; color: red'

def style_cell_humid (value):
    limit1 = 30; limit2 = 50
    if value < limit1:
        return 'background-color: orange; color: black'
    elif (value >= limit1) & (value <= limit2):
        return 'background-color: lightgreen; color: black'
    elif (value > limit2):
        return 'background-color: lightblue; color: black'
    elif pd.isna(value):
        return 'background-color: white; color: red'

def style_co2_column (value):
    limit1 = 400; limit2 = 1000; limit3 = 2000; limit4 = 5000; limit5 = 40000
    if value <= limit1:
        return 'background-color: lightgreen; color: black'
    elif (value > limit1) & (value <= limit2):
        return 'background-color: lightgreen; color: black'
    elif(value > limit2) & (value <= limit3):
        return 'background-color: yellow; color: black'
    elif(value > limit3) & (value <= limit4):
        return 'background-color: orange; color: black'
    elif(value > limit4) & (value <= limit5):
        return 'background-color: red; color: black'
    elif value > limit5:
        return 'background-color: darkred; color: black'
    #elif pd.isna(value):
        #return 'background-color: white; color: red'

def style_temp_column (value):
    limit1 = 20; limit2 = 26
    if value < limit1:
        return 'background-color: lightblue; color: black'
    elif (value >= limit1) & (value <= limit2):
        return 'background-color: lightgreen; color: black'
    elif (value > limit2):
        return 'background-color: red; color: black'

def style_humid_column (value):
    limit1 = 30; limit2 = 50
    if value < limit1:
        return 'background-color: orange; color: black'
    elif (value >= limit1) & (value <= limit2):
        return 'background-color: lightgreen; color: black'
    elif (value > limit2):
        return 'background-color: lightblue; color: black'