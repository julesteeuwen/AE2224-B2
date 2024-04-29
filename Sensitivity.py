# calculates sensitivy of the models to the indicators
# import stuff
import pandas as pd
import csv

# make new dataframes
def make_new_DF(file, ansp, sensi_parameter = 0.9):
    dataframe = pd.read_csv(file, index_col= 'FLT_DATE',parse_dates=True, date_format='%d-%m-%Y',delimiter=';').dropna()
    dataframe = dataframe[dataframe['ENTITY_NAME'] == ansp]
    
    

# train existing models on the new dataframes

# compare the new models to the old models

# plot the results

#execute the functions