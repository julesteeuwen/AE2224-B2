import pandas as pd
import pmdarima as pm
from pmdarima import model_selection
import numpy as np
from matplotlib import pyplot as plt
from pmdarima.preprocessing import FourierFeaturizer
from pmdarima import pipeline


# Load the data and split it into separate pieces
dataframe = pd.read_csv('Datasets/2017-2019.csv', index_col= 'FLT_DATE',parse_dates=True, date_format='%d-%m-%Y',delimiter=';')
dataframe = dataframe.dropna()  # drop missing values
df1 = dataframe[dataframe['ENTITY_NAME'] == 'LVNL']
field = 'CPLX_INTER'
data = df1[field].values
train, test = model_selection.train_test_split(df1[field], train_size=0.75)

# #############################################################################

pipe = pipeline.Pipeline([
    ("fourier", FourierFeaturizer(m=365)),
    ("arima", pm.AutoARIMA(stepwise=True, trace=10, error_action="ignore",
                              seasonal=False,  # because we use Fourier
                              suppress_warnings=True))
                              ])
pipe.fit(y=train.values)

# #############################################################################
# Plot actual test vs. forecasts:
plt.plot(train, color='blue',label='Train samples')
plt.plot(test, color='red',label='Test samples')
plt.plot(test.index,pipe.predict(n_periods=len(test.values)),label='Forecasts')
plt.title('Actual test samples vs. forecasts')
plt.legend()
plt.show()
