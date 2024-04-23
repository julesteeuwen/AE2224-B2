import pandas as pd
import matplotlib.pyplot as plt
from preprocessing import read_data
from sklearn.model_selection import train_test_split
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np
import seaborn as sns
from pmdarima.arima import auto_arima

df = read_data('Datasets/split_2014-2016.csv')
df = df[df['ENTITY_NAME'] == "LVNL"]

def autocorrelation(dataframe, label, plotting = False):
    """
    prints or plots the atuocorrelation of the dataframe
    """
    autocorrelation_lag1 = dataframe[label].autocorr(lag=1)
    autocorrelation_lag30 = dataframe[label].autocorr(lag=30)
    autocorrelation_lag60 = dataframe[label].autocorr(lag=60)
    autocorrelation_lag180 = dataframe[label].autocorr(lag=180)
    autocorrelation_lag360 = dataframe[label].autocorr(lag=360)
    if plotting:
        x = pd.plotting.autocorrelation_plot(dataframe[label])
        plt.title("Autocorrelation plot",color = 'green')
        x.plot()
        plt.draw()
        plt.show()
    else:
        print("one day lag: ", autocorrelation_lag1)
        print("30 day lag: ", autocorrelation_lag30)
        print("60 day lag: ", autocorrelation_lag60)
        print("180 day lag: ", autocorrelation_lag180)
        print("360 day lag: ", autocorrelation_lag360)

def Trend_Decompose(dataframe, label, plotting = False):
    decompose = seasonal_decompose(dataframe[label], model = 'additive', period = 7)
    trend = decompose.trend
    seasonal = decompose.seasonal
    residual = decompose.resid
    ax = seasonal.plot(label='Seasonality', color='blue')
    min_ = seasonal.idxmin()
    max_ = seasonal.idxmax()
    min_2 = seasonal[max_:].idxmin()
    max_2 = seasonal[min_2:].idxmax()
    ax.axvline(min_,label='min 1',c='red')
    ax.axvline(min_2,label='min 2',c='red', ls=':')
    ax.axvline(max_,label='max 1',c='green')
    ax.axvline(max_2,label='max 2',c='green', ls=':')
    plt.legend(loc='upper right', fontsize='x-small')
    print(f'The time difference between the two minimums is {min_2-min_}')
    ax.plot()
    plt.show()

def auto_ARIMA(dataframe, label, test_size, plotting = False):
    train, test = train_test_split(dataframe, test_size = test_size, shuffle=False)
    model = auto_arima(x=train.index, y=train[label].values, trace=True, error_action='ignore', suppress_warnings=True)
    model.fit(x=train.index, y=train[label].values)
    forecast = model.predict(n_periods=len(test))
    forecast = pd.DataFrame(forecast, index = test.index, columns = ['Prediction'])
    if plotting:
        plt.plot(test.index, np.array(forecast),color = 'blue')
        plt.plot(test.index, test[label], color = 'red')
        plt.show()




#autocorrelation(df, "HORIZ_INTER_HRS", plotting =True)
#Trend_Decompose(df, "HORIZ_INTER_HRS", plotting =True)
auto_ARIMA(df, "VERTICAL_INTER_HRS", test_size = 0.2, plotting = True)