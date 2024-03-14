import pandas as pd
import numpy as np
import statsmodels as sm
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller

def read_data(filename):
    """
    Reads all of the data from the file, returns the data as a dataframe
    """
    dataframe = pd.read_csv(filename)
    dataframe = dataframe.dropna()
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
    if ANSPName not in ANSPs:
        print('Invalid ANSP name')
        ANSPName = input('Input correct ANSP name')
    else:
        ANSPIndex = ANSPs.index(ANSPName)
    return ANSPsdf[ANSPIndex]

def Fuller_test(dataframe, parameter, plotting=False):
    """
    Checks if the parameter is stationary, returns True of stationary, False if not
    """
    dataframe["FLT_Date"] = pd.to_datetime(dataframe["FLT_DATE"], format=r"%d-%m-%Y")   
    dataframe.index = dataframe["FLT_Date"]
    rolling_mean = dataframe[parameter].rolling(15).mean()
    print(rolling_mean)
    rolling_std = dataframe[parameter].rolling(15).std()
    '''
    error_mean = 0
    error_std = 0
    for i in range(12,len(dataframe[parameter])):
        error_mean += (dataframe[parameter][i] - rolling_mean[i])
        error_std += (dataframe[parameter][i] - rolling_std[i])
    print(f"mean error = {error_mean/len(dataframe[parameter])}, std error = {error_std/len(dataframe[parameter])}")
    '''
    if plotting:
        plt.plot(np.array(dataframe["FLT_Date"].values), np.array(dataframe[parameter].values), label='Data', color = "red")
        plt.plot(rolling_mean, color = "blue", label = "Rolling Mean")
        plt.plot(rolling_std, color = "green", label = "Rolling Std")
        plt.legend(loc = "best")
        plt.draw()
        plt.show()
    adft = adfuller(np.array(dataframe[parameter].values), autolag='AIC')
    if adft[1] < 0.05:
        print(f"{parameter} is stationary")
        return True
    else:
        print(f"{parameter} is not stationary")
        return False

dataframe = read_data('Datasets/split_2014-2016.csv')
dataframe = dataframe[dataframe['ENTITY_NAME'] == "LVNL"]
Fuller_test(dataframe, "CPLX_FLIGHT_HRS")


