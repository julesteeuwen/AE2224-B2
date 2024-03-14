import pandas as pd
import numpy as np

def read_data(filename):
    """
    Reads all of the data from the file, returns the data as a dataframe
    """
    dataframe = pd.read_csv(filename, index_col= 'FLT_DATE',parse_dates=True, date_format='%d-%m-%Y')
    
    return dataframe

def ANSPs(SortedData):
    """
    Takes the sorted dataframe and returns a list of all of the ANSPs
    """
    ANSPs = []
    return SortedData.ENTITY_NAME.unique()

def cleanlist(list):
    list = [x for x in list if str(x) != 'nan']
    return list

def split_data(SortedData, ANSPs):
    """
    Takes the sorted dataframe and splits into seperate dataframes for each ANSP, returns a list containing all of these dataframes
    """
    ANSPsdf = [] 

    for ANSP in ANSPs:
        grouped = SortedData.groupby(SortedData.ENTITY_NAME)
        ANSP = grouped.get_group(ANSP)
        ANSPsdf.append(ANSP)
    return ANSPsdf

def get_data(ANSPName, ANSPsdf, ANSPs):
    """
    Takes a given ANSP name and returns the dataframe for that ANSP
    """
    while ANSPName not in ANSPs:
        print('Invalid ANSP name')
        ANSPName = input('Input correct ANSP name')
    ANSPIndex = ANSPs.index(ANSPName)
    return ANSPsdf[ANSPIndex], ANSPName

