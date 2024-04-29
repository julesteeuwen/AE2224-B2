import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error as mse
import sys
from complexity_calculation import calculate_scores_daily

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

# Holt-Winters triple exponential smoothing method, single, double and triple exponential smoothing using additive or multiplicative multiplaction
def HWES3_ADD(df, period=365):
    return ExponentialSmoothing(df, trend='add', seasonal='add', seasonal_periods=period).fit().fittedvalues

def HWES3_MUL(df, period=365):
    return ExponentialSmoothing(df, trend='mul', seasonal='mul', seasonal_periods=period).fit().fittedvalues

def HWES2_ADD(df):
    return ExponentialSmoothing(df, trend='add').fit().fittedvalues

def HWES2_MUL(df):
    return ExponentialSmoothing(df, trend='mul').fit().fittedvalues

def HWES1(df, period=365):
    alpha = 1/(2*period)
    return SimpleExpSmoothing(df).fit(smoothing_level=alpha, optimized=False, use_brute=True).fittedvalues

def HWES2(df):
    return ExponentialSmoothing(df, trend='add').fit().fittedvalues



def plot_forecast_HWES3_ADD(df, period=365, field='CPLX_INTER'):
    # Calculate daily complexity scores
    df = calculate_scores_daily(df)

    # Filtering data and selecting an ANSP
    df_vert = df.loc[:, field].to_frame()
    df_ansp = df_vert.loc[df['ENTITY_NAME'] == 'Skyguide'].copy()
    df_ansp.index.freq = pd.infer_freq(df_ansp.index)

    # Split data
    slice = int(0.75*len(df_ansp))
    train_ansp = df_ansp[:slice].copy()
    test_ansp = df_ansp[slice:]

    # Fit and predict model
    model = ExponentialSmoothing(train_ansp, trend='add', seasonal='add', seasonal_periods=period).fit()
    predicted_values = model.forecast(len(test_ansp))

    # Calculate RMSE (Stijn's Method vs Statsmodels)
    score = 0
    for i in range(len(test_ansp)):
        score += (test_ansp.values[i] - predicted_values[i])**2
    print(f'Stijn Score: {score**0.5/len(test_ansp.values)}')

    rmse = np.sqrt(mse(test_ansp, predicted_values))
    print(f'RMSE Score: {rmse}')

    # Plot results
    train_ansp[field].plot(legend=True, label='TRAIN')
    test_ansp[field].plot(legend=True, label='TEST')
    predicted_values.plot(legend=True, label='pred')

    plt.show()


# Importing data
df = pd.read_csv('Datasets/split_2014-2016.csv', index_col='FLT_DATE', parse_dates=True, date_format='%d-%m-%Y')
df.dropna(inplace=True)

# Filtering data and selecting an ANSP
df_vert = df.loc[:, "VERTICAL_INTER_HRS"].to_frame()
df_ansp = df_vert.loc[df['ENTITY_NAME'] == 'ROMATSA'].copy()
df_ansp.index.freq = pd.infer_freq(df_ansp.index)

decomp_data = plot_decompose(df_ansp)
print(decomp_data.trend)


# df_ansp.loc[:, "SMA"] = SMA(df_ansp, 50)
# df_ansp.loc[:, "CMA"] = CMA(df_ansp.loc[:, 'VERTICAL_INTER_HRS'])
# df_ansp.loc[:, "EWMA"] = EWMA(df_ansp.loc[:, 'VERTICAL_INTER_HRS'], 50)

# print(HWES3_ADD(df_ansp).size)
# print(df_ansp.size)

# Split data
slice = int(0.8*len(df_ansp))
train_ansp = df_ansp[:slice]
test_ansp = df_ansp[slice:]

# Fit and predict model
model = ExponentialSmoothing(train_ansp, trend='add', seasonal='add', seasonal_periods=365).fit()
test_predictions = model.forecast(365)

# Plot results
train_ansp['VERTICAL_INTER_HRS'].plot(legend=True, label='TRAIN')
test_ansp['VERTICAL_INTER_HRS'].plot(legend=True, label='TEST')
test_predictions.plot(legend=True, label='pred')



# df_ansp.loc[:, "HWES3_ADD"] = HWES3_ADD(df_ansp)
# df_ansp.loc[:, "HWES3_MUL"] = HWES3_MUL(df_ansp[["VERTICAL_INTER_HRS"]])



# df_ansp[["HWES3_MUL"]] = HWES3_MUL(df_ansp)




# df_ansp.plot()
plt.show()

