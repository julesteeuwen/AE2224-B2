import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import preprocessing
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Simple Moving Average (SMA)
def SMA(df, period):
    """ Returns a dataframe containing the Simple Moving Averages over the given dataframe using the given period """
    return df.rolling(period).mean()

# Cumulative Moving Average (CMA)
def CMA(df):
    """ Returns a dataframe containing the Cumulative Moving Averages over the given dataframe """
    return df.expanding().mean()

# Weighted Moving Average (WMA)
def WMA(df, period):
    """ Returns a dataframe containing the (Linearly) Weighted Moving Averages over the given dataframe using the given period """
    return

# Exponentially Weighted Moving Average (EWMA)
def EWMA(df, period):
    """ Returns a dataframe containing the Exponentially Weighted Moving Averages over the given dataframe using the given period """
    return df.ewm(span=period).mean()

def plot_decompose(df):
    result = seasonal_decompose(df, model='multiplicative', period=365)
    result.plot()
    plt.show()
    return result

# Holt-Winters triple exponential smoothing method
def HoltWinters():
    return

# Importing data
df = pd.read_csv('Datasets/split_2014-2016.csv', index_col='FLT_DATE', parse_dates=True, date_format='%d-%m-%Y')
df.dropna(inplace=True)

# Filtering data and selecting an ANSP
df_vert = df.loc[:, "VERTICAL_INTER_HRS"].to_frame()
df_ansp = df_vert.loc[df['ENTITY_NAME'] == 'ROMATSA'].copy()
df_ansp.index.freq = pd.infer_freq(df_ansp.index)

decomp_data = plot_decompose(df_ansp)
print(decomp_data.trend)


df_ansp.loc[:, "SMA"] = SMA(df_ansp, 50)
df_ansp.loc[:, "CMA"] = CMA(df_ansp.loc[:, 'VERTICAL_INTER_HRS'])
df_ansp.loc[:, "EWMA"] = EWMA(df_ansp.loc[:, 'VERTICAL_INTER_HRS'], 50)

df_ansp.plot()
plt.show()

