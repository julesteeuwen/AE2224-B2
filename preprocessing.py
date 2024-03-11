import pandas as pd
import numpy as np

def read_data(filename):
    """
    Reads all of the data from the file, returns the data as a dataframe
    """

    
    return dataframe

def sort_data(df):
    """
    Takes the dataframe and sorts it by ANSP, returns data as the sorted dataframe
    """
    SortedData = df.sort_values(['ENTITY_NAME','FLT_DATE'])
    return SortedData