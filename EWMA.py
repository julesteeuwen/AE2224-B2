import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Simple Moving Average (SMA)
df = pd.read_csv('Datasets/AAPL.csv')
df = df[['Date', 'Close']]

# preprocessing to make dates "date" data type
def date(df):
    
    
    
    return

def SMA(df, period):
    
    # Split the data into timeframes with period datapoints.
    df['MA'] = df[['Close']].rolling(period).mean()

    # Calculate the average for each timeframe
    return df




# Weighted Moving Average (WMA)
    


# Exponentially Weighted Moving Average (EWMA)

# Plotting data
print(df)
x = [0, 1, 2, 3]
y = [4, 6, 7, 8]
df.plot()
print(df.dtypes)
plt.show()

