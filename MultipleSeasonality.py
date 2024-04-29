
import matplotlib.pyplot as plt
import pandas as pd
from complexity_calculation import calculate_scores_daily
from preprocessing import *
from statsmodels.tsa.seasonal import MSTL
from statsmodels.tsa.seasonal import DecomposeResult

# Sktime imports
from sktime.forecasting.tbats import TBATS
from sktime.forecasting.statsforecast import StatsForecastAutoTBATS
from sktime.utils.plotting import plot_series

from sklearn.metrics import mean_squared_error as mse
from statsforecast import StatsForecast
import pickle

def MultipleSeasonalityDecomp(df, iterate):
    # mstl = MSTL(df, periods=[7, 365])
    
    print("I am working")
    model = [MSTL(season_length=[7,365])]
    sf = StatsForecast(models = model, freq = 'W')
    sf = sf.fit(df = df)
    sf.fitted_[0, 0].model_.tail(24 * 28).plot(subplots=True, grid=True)
    plt.tight_layout()
    plt.show()
    # forecasts = sf.predict()
    # res = mstl.fit()
    # res.plot()
    # plt.show()
    
    # sf.dshw(df, period1 = 7, period2 = 365, h = 365)

def forecast_TBATS(df, periods):
    # Split data
    slice = int(0.75*len(df))
    train = df[:slice].copy()
    test = df[slice:]

    # Fit and predict model
    model = TBATS(sp=periods, use_trend=True, use_box_cox=True, use_damped_trend=True)
    # print(train)
    model.fit(train)
    fh = np.arange(len(test))
    predicted_values = model.predict(fh)

    plot_series(train, test, predicted_values, labels=['Train', 'Test', 'Predicted'])
    plt.show()

    # Calculate MSE
    # MSE = mse(test, predicted_values)

    return train, test, predicted_values

def calculateModel():
    for ANSP in ANSPs:
        for field in fields:
            # Selecting an ANSP
            df_ansp = df.loc[df['ENTITY_NAME'] == ANSP].copy()

            # Calculate daily complexity scores
            df_scores = calculate_scores_daily(df_ansp)

            # Filtering data and selecting an ANSP
            df_field = df_scores[field]
            df_field.index.freq = pd.infer_freq(df_field.index)
            # Split data
            slice = int(0.75*len(df_ansp))
            train = df[:slice].copy()
            test = df[slice:]

            model = StatsForecastAutoTBATS(train).fit()

            # Save to Pickle
            pickle.dump(model, open(f"TBATS/{ANSP}{field}.pkl", 'wb'))

# Variables
periods = [365, 7]
fields = ['CPLX_FLIGHT_HRS', 'CPLX_INTER', 'HORIZ_INTER_HRS', 'SPEED_INTER_HRS', 'VERTICAL_INTER_HRS']
ANSPs = ['Skyguide', 'DSNA', 'MUAC']

# Importing data
df = pd.read_csv('Datasets/split_2017-2019.csv', index_col='FLT_DATE', parse_dates=True, date_format='%d-%m-%Y')
df.dropna(inplace=True)

