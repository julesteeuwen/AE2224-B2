import pandas as pd
from sklearn.metrics import mean_squared_error as mse
from sktime.utils.plotting import plot_series
import matplotlib.pyplot as plt
import numpy as np

from EWMA import plot_prediction

from complexity_calculation import calculate_scores_daily

from sktime.forecasting.tbats import TBATS

# Read data
df = pd.read_csv('Datasets/split_2017-2019.csv', index_col='FLT_DATE', parse_dates=True, date_format='%d-%m-%Y')
df.dropna(inplace=True)
df.index.freq = pd.infer_freq(df.index)

periods = [365]

df_ansp = df.loc[df['ENTITY_NAME'] == 'Skyguide'].copy()
df_scores = calculate_scores_daily(df_ansp)
df_field = df_scores.loc[:, 'Complexity_score'].to_frame()

slice = int(0.75 * len(df_field))
train = df_field[:slice]
test = df_field[slice:]

model = TBATS(sp=periods).fit(train)

fh = np.arange(len(test))
predicted_values = model.predict(fh)

mse = mse(test, predicted_values)
print('MSE: ', mse)

plot_series(train, test, predicted_values, labels=['Train', 'Test', 'Predicted'])
plt.show()

