import pandas as pd
import numpy as np

def read_data(filename):
    """
    Reads all of the data from the file, returns the data as a dataframe
    """
    dataframe = pd.read_csv(filename)

    
    return dataframe

def sort_data(dataframe):
    """
    Takes the dataframe and sorts it by ANSP, returns data as the sorted dataframe
    """
    SortedData = dataframe.sort_values(['ENTITY_NAME','FLT_DATE'])
    return SortedData

def ANSPs(SortedData):
    """
    Takes the sorted dataframe and returns a list of all of the ANSPs
    """
    ANSPs = []
    for i in range(len(SortedData.loc[:,['ENTITY_NAME']])):
        ANSP = SortedData.ENTITY_NAME[i]
        if ANSP not in ANSPs:
            ANSPs.append(ANSP)
    return ANSPs

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
    return ANSPsdf[ANSPIndex]

