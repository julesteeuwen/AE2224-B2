import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error as mse
from complexity_calculation import calculate_scores_daily
import csv

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
    return ExponentialSmoothing(df, trend='add', seasonal='add', seasonal_periods=period).fit()

def HWES3_MUL(df, period=365):
    return ExponentialSmoothing(df, trend='mul', seasonal='mul', seasonal_periods=period).fit()

def HWES2_ADD(df):
    return ExponentialSmoothing(df, trend='add').fit()

def HWES2_MUL(df):
    return ExponentialSmoothing(df, trend='mul').fit()

def HWES1(df, period=365):
    alpha = 1/(2*period)
    return SimpleExpSmoothing(df).fit(smoothing_level=alpha, optimized=False, use_brute=True)

def HWES2(df):
    return ExponentialSmoothing(df, trend='add').fit()

def plot_prediction(train, test, predicted_values):
    train.plot(legend=True, label='TRAIN')
    test.plot(legend=True, label='TEST')
    predicted_values.plot(legend=True, label='Predicted')

def computeModel(df, ANSP, field):
    # Filtering data and selecting an ANSP
    df_ansp = df.loc[df['ENTITY_NAME'] == ANSP].copy()

    df_scores = calculate_scores_daily(df_ansp)

    df_field = df_scores.loc[:, field].to_frame()
    df_field.index.freq = pd.infer_freq(df_field.index)

    slice = int(0.75 * len(df_field))
    train = df_field[:slice]
    test = df_field[slice:]

    model = HWES3_ADD(train, period=365)

    pickle.dump(model, open(f"HWES_ADD/{ANSP}{field}.pkl", 'wb'))
    return model

########################################################################################


def main(plotting=False):
    fields = ['CPLX_FLIGHT_HRS', 'CPLX_INTER', 'HORIZ_INTER_HRS', 'SPEED_INTER_HRS', 'VERTICAL_INTER_HRS', 'Complexity_score']
    ANSPs = ['Skyguide', 'DSNA', 'MUAC']

    # Importing data
    df = pd.read_csv('Datasets/split_2017-2019.csv', index_col='FLT_DATE', parse_dates=True, date_format='%d-%m-%Y')
    df.dropna(inplace=True)
    df = calculate_scores_daily(df)

    for ANSP in ANSPs:
        predicted_values = pd.DataFrame()
        test_values = pd.DataFrame()
        train_values = pd.DataFrame()
        mse_componentwise = None
        mse_total = None

        for field in fields:
            # Check if model already exists
            try:
                model = pickle.load(open(f"HWES_ADD/{ANSP}{field}.pkl", 'rb'))
            except:
                model = computeModel(df, ANSP, field)

            # Get test data
            df_ansp = df.loc[df['ENTITY_NAME'] == ANSP].copy()
            df_field = df_ansp.loc[:, field].to_frame()
            df_field.index.freq = pd.infer_freq(df_field.index)
            slice = int(0.75 * len(df_field))
            train = df_field[:slice]
            test = df_field[slice:]

            # Update dataframe
            predicted_values[field] = model.forecast(len(test))
            test_values[field] = test
            train_values[field] = train

            if field == 'Complexity_score':
                mse_total = mse(test, predicted_values[field])


        predicted_complexity = calculate_scores_daily(predicted_values.copy())

        test_complexity = calculate_scores_daily(test_values)
        mse_componentwise = mse(test_complexity['Complexity_score'], predicted_complexity['Complexity_score'])

        # Plotting
        if plotting:
            fig, axs = plt.subplots(2, 1) 
            axs[0].set_title(f'{ANSP} - Componentwise Prediction')
            train_values['Complexity_score'].plot(legend=True, label='Train', ax=axs[0])
            test_complexity['Complexity_score'].plot(legend=True, label='Test', ax=axs[0])
            predicted_complexity['Complexity_score'].plot(legend=True, label='Predicted', ax=axs[0])

            axs[1].set_title(f'{ANSP} - Total Prediction')
            train_values['Complexity_score'].plot(legend=True, label='Train', ax=axs[1])
            test_complexity['Complexity_score'].plot(legend=True, label='Test', ax=axs[1])
            predicted_values['Complexity_score'].plot(legend=True, label='Predicted', ax=axs[1])
            plt.show()

            # Plot componentwise component predictions in one figure
            fig, axs = plt.subplots(len(fields), 1)
            for field in fields:
                axs[fields.index(field)].set_title(f'{ANSP} - {field}')
                train_values[field].plot(legend=True, label='Train', ax=axs[fields.index(field)])
                test_values[field].plot(legend=True, label='Test', ax=axs[fields.index(field)])
                predicted_values[field].plot(legend=True, label='Predicted', ax=axs[fields.index(field)])
            plt.show()

        print(f"{ANSP} Total MSE: {mse_total}")
        print(f"{ANSP} Componentwise MSE: {mse_componentwise}")

if __name__ == '__main__':
    main(plotting=True)
    

 










