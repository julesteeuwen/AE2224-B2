#import stuff
import pandas as pd
import matplotlib.pyplot as plt

#get values
def get_values(file, ansp):
    dataframe = pd.read_csv(file, index_col= 'FLT_DATE',parse_dates=True, date_format='%d-%m-%Y',delimiter=';').dropna()
    dataframe = dataframe[dataframe['ENTITY_NAME'] == ansp]
    VERTICAL_INTER_HRS = dataframe['VERTICAL_INTER_HRS']
    HORIZ_INTER_HRS = dataframe['HORIZ_INTER_HRS']
    SPEED_INTER_HRS = dataframe['SPEED_INTER_HRS']
    CPLX_INTER = dataframe['CPLX_INTER']
    CPLX_FLIGHT_HRS = dataframe['CPLX_FLIGHT_HRS']
    return VERTICAL_INTER_HRS, HORIZ_INTER_HRS, SPEED_INTER_HRS, CPLX_INTER, CPLX_FLIGHT_HRS

#calculations

#plotting

print(get_values('Datasets/2017-2019.csv', 'Skyguide')[0])
