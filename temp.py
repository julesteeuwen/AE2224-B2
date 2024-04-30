import pandas as pd
from sklearn.metrics import mean_squared_error as mse
from sktime.utils.plotting import plot_series
import matplotlib.pyplot as plt

# Read data
df = pd.read_csv('Datasets/split_2017-2019.csv', index_col='FLT_DATE', parse_dates=True, date_format='%d-%m-%Y')
df.dropna(inplace=True)
