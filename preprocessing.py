import pandas as pd
import numpy as np
import statsmodels as sm
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
from arch.unitroot import PhillipsPerron
from scipy.stats import kruskal

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


def Stationary_test(dataframe, parameter, plotting=False):
    """
    Checks if dataframe is stationary, prints the results in terminal
    """
    #Dickey-Fuller Test
    dataframe.dropna()
    rolling_mean = dataframe[parameter].rolling(15).mean()

def Fuller_test(dataframe, parameter, plotting=False):
    """
    Checks if the parameter is stationary, returns True of stationary, False if not
    """
    dataframe.dropna()
    #dataframe["FLT_Date"] = pd.to_datetime(dataframe["FLT_DATE"], format=r"%d-%m-%Y")   
    #dataframe.index = dataframe["FLT_Date"]
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

        plt.plot(np.array(dataframe.index), np.array(dataframe[parameter].values), label='Data', color = "red")
      
        plt.plot(rolling_mean, color = "blue", label = "Rolling Mean")
        plt.plot(rolling_std, color = "green", label = "Rolling Std")
        plt.legend(loc = "best")
        plt.draw()
        plt.show()
    adft = adfuller(np.array(dataframe[parameter].values), autolag='AIC')

    print(f"ADF-test:{parameter} = {adft[1]}")
    '''
    if adft[1] < 0.05:
        print(f"DF-test:{parameter} is stationary")
    else:
        print(f"DF-test:{parameter} is not stationary")
    '''
    
    # Phillips-Perron Test
    pp = PhillipsPerron(dataframe[parameter],trend = 'ct', test_type="rho")
    print(pp.summary().as_text())
    '''
    if pp.pvalue < 0.05:
        print(f"PP-test:{parameter} is stationary")
    else:
        print(f"PP-test:{parameter} is not stationary")
    '''


def seasonality_check(series, period=365):
    """
    This function performs the Kruskal-Wallis H-test, to determine if the series has a seasonal component.
    Input: Series that should be tested (not dataframe :))
           Seasonal period (default 365)
    Output: True / False
    """
    idx = np.arange(len(series.index)) % period
    H_statistic, p_value = kruskal(series, idx)
    return p_value <= 0.05

#dataframe = read_data('Datasets/split_2014-2016.csv')
#dataframe = dataframe[dataframe['ENTITY_NAME'] == "LVNL"]
#Fuller_test(dataframe, "CPLX_FLIGHT_HRS")



#dataframe = read_data('Datasets/split_2014-2016.csv')
#dataframe = dataframe[dataframe['ENTITY_NAME'] == "LVNL"]
#Stationary_test(dataframe, "CPLX_FLIGHT_HRS", plotting = True)