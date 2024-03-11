import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Simple Moving Average (SMA)
df = pd.read_csv('Datasets/AAPL.csv')
df = df[['Close']]

# preprocessing to make dates "date" data type
def date(df):
    
    
    
    return

def SMA(df, period):
    """ Adds a column 'SMA' with the moving averages using the given period"""
    
    df['SMA'] = df.rolling(period).mean()

    return df

# Cumulative Moving Average (CMA)
def CMA(df):

    df['CMA'] = df.rolling().expanding().mean()

    return df

# Weighted Moving Average (WMA)
def WMA(df, period):

    return df

# Exponentially Weighted Moving Average (EWMA)
def EWMA(df, period):

    df['EWMA'] = df.rolling(period).ewm(period).mean()

# Plotting data
print(df)
x = [0, 1, 2, 3]
y = [4, 6, 7, 8]
df.plot()
print(df.dtypes)
plt.show()


    return df