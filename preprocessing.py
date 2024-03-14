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


