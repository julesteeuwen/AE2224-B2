import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf

#import data
df = pd.read_csv('Datasets/AAPL.csv')
df = df[['Date', 'Close']]
df['Date'] = pd.to_datetime(df['Date'], format = '%Y-%m-%d')
df.set_index(['Date'], inplace = True)

#check stationarity
test_result=adfuller(df['Close'])

def adfuller_test(sales):
    result=adfuller(sales)
    labels = ['ADF Test Statistic','p-value','#Lags Used','Number of Observations Used']
    for value,label in zip(result,labels):
        print(label+' : '+str(value) )
    if result[1] <= 0.05:
        print("P value is less than 0.05 that means we can reject the null hypothesis(Ho). Therefore we can conclude that data has no unit root and is stationary")
    else:
        print("Weak evidence against null hypothesis that means time series has a unit root which indicates that it is non-stationary ")

#adfuller_test(df['Close'])

#Differencing
df['Daily First Difference']=df['Close']-df['Close'].shift(1)
#adfuller_test(df['Daily First Difference'].dropna())

#fig = plt.figure(figsize=(12,8))
#ax1 = fig.add_subplot(211)
#fig = sm.graphics.tsa.plot_acf(df['Daily First Difference'].iloc[13:],lags=40,ax=ax1)
#ax2 = fig.add_subplot(212)
#fig = sm.graphics.tsa.plot_pacf(df['Daily First Difference'].iloc[13:],lags=40,ax=ax2)
#plt.show()

model=sm.tsa.statespace.SARIMAX(df['Close'],order=(1, 1, 1),seasonal_order=(1,1,1,12))
results=model.fit()
print(results.summary())

#residuals = pd.DataFrame(results.resid)
#residuals.plot()
#plt.show()
# density plot of residuals
#residuals.plot(kind='kde')
#plt.show()
# summary stats of residuals
#print(residuals.describe())

df['forecast']=results.predict(start=200,end=250,dynamic=True)
df[['Close', 'forecast']].plot(figsize=(12,8))
plt.show()