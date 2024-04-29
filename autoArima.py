from sklearn.metrics import mean_squared_error
import pandas as pd
import pmdarima as pm
from pmdarima import model_selection
import numpy as np
from matplotlib import pyplot as plt
from pmdarima.preprocessing import FourierFeaturizer
from pmdarima import pipeline
import joblib

def get_test_data(ANSP, field):
    dataframe = pd.read_csv('Datasets/2017-2019.csv', index_col= 'FLT_DATE',parse_dates=True, date_format='%d-%m-%Y',delimiter=';')
    dataframe = dataframe.dropna()  # drop missing values
    df1 = dataframe[dataframe['ENTITY_NAME'] == ANSP]
    train, test = model_selection.train_test_split(df1[field], train_size=0.75)
    return test

def get_SARIMA(ANSP, field,graph=False):
    print(f'Getting SARIMA model for {ANSP} and {field}')
    print('Wait a moment... or two.... or three...')
    # Load the data and split it into separate pieces
    dataframe = pd.read_csv('Datasets/2017-2019.csv', index_col= 'FLT_DATE',parse_dates=True, date_format='%d-%m-%Y',delimiter=';')
    dataframe = dataframe.dropna()  # drop missing values
    df1 = dataframe[dataframe['ENTITY_NAME'] == ANSP]
    train, test = model_selection.train_test_split(df1[field], train_size=0.75)

    # #############################################################################

    pipe = pipeline.Pipeline([
        ("fourier", FourierFeaturizer(m=365)),
        ("arima", pm.AutoARIMA(stepwise=True, trace=10, error_action="ignore",
                                  seasonal=False,  # because we use Fourier
                                  suppress_warnings=True))
                                  ])
    pipe.fit(y=train.values)

    '''
    #score function
    score = 0
    predicted_values = pipe.predict(n_periods=len(test.values)).values
    for i in range(len(test)):
        score += (test.values[i] - predicted_values[i])**2
    print(f'Score: {score/len(test.values)}')
    '''
    # #############################################################################
    #save  the model to a file

    joblib.dump(pipe, f'SARIMAS/{ANSP}{field}.pkl')
    print(f'SARIMA model for {ANSP} and {field} saved to SARIMAS/{ANSP}{field}.pkl')
    # #############################################################################
    if not graph:
        return pipe
    print(mean_squared_error(test, pipe.predict(n_periods=len(test.values))))
    # Plot actual test vs. forecasts:
    plt.plot(train, color='blue',label='Train samples')
    plt.plot(test, color='red',label='Test samples')
    plt.plot(test.index,pipe.predict(n_periods=len(test.values)),label='Forecasts')
    plt.title('Actual test samples vs. forecasts')
    plt.legend()
    plt.show()
    return pipe
