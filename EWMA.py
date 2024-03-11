import pandas as pd
import numpy as np


# Simple Moving Average (SMA)
df = pd.read_csv('Datasets/AAPL.csv')
df = df[['Date', 'Close']]

def SMA(df, period):
    
    # Split the data into timeframes with period datapoints.
    df['MA'] = df[['Close']].rolling(period).mean()

    # Calculate the average for each timeframe
    return df

print(SMA(df, 5))



# Weighted Moving Average (WMA)
    


# Exponentially Weighted Moving Average (EWMA)
