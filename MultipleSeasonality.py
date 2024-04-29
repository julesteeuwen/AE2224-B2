
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import numpy as np
import seaborn as sns
import forecast
from preprocessing import *
from statsforecast import StatsForecast
from statsforecast.models import MSTL, AutoARIMA
from pandas.plotting import register_matplotlib_converters
#from statsmodels.tsa.seasonal import MSTL
from statsmodels.tsa.seasonal import DecomposeResult

def readfilemultipleseason(filename):
    df = pd.read_csv(filename,parse_dates=True, date_format='%d-%m-%Y')
    return df



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