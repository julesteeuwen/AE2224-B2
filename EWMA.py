import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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



# Importing data
df = pd.read_csv('Datasets/AAPL.csv')
df_close = df[['Close']]

df[['SMA']] = SMA(df_close, 10)
df[['CMA']] = CMA(df_close)
df[['EWMA']] = EWMA(df_close, 10)


# Plotting data
df = df[['Date', 'Close', 'SMA', 'CMA', 'EWMA']]

df['Date'] = pd.to_datetime(df['Date'], format = '%Y-%m-%d')

df.set_index(['Date'], inplace = True)

print(df)
df.plot()
print(df.dtypes)
plt.show()

