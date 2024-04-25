#import stuff
import pandas as pd

#get values\
def get_values(file, ansp):
    dataframe = pd.read_csv(file, index_col= 'FLT_DATE',parse_dates=True, date_format='%d-%m-%Y',delimiter=';').dropna()
    #dataframe = dataframe.dropna()  # drop missing values
    dataframe = dataframe[dataframe['ENTITY_NAME'] == ansp]
    print(dataframe)
    CPLX_INTER = 0
    CPLX_FLIGHT_HRS = 0
    I_INTER_HRS = 0
    return CPLX_INTER, CPLX_FLIGHT_HRS, I_INTER_HRS

#calculations

#plotting

print(get_values('Datasets/2017-2019.csv', 'Skyguide')[0])
