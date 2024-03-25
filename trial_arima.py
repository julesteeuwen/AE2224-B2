from preprocessing import read_data
from pmdarima.arima import auto_arima
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

dataframe = pd.read_csv(('Datasets/split_2014-2016.csv'),parse_dates=True, date_format='%d-%m-%Y')
dataframe = dataframe[dataframe['ENTITY_NAME'] == "LVNL"]

train, test = train_test_split(dataframe, test_size=0.2, shuffle=False)

plt.plot(np.array(train["FLT_DATE"].values), np.array(train["VERTICAL_INTER_HRS"].values), color = "black")
plt.plot(np.array(test["FLT_DATE"].values), np.array(test["VERTICAL_INTER_HRS"].values), color = "red")
#sns.set()


model = auto_arima(x=train["FLT_DATE"].values,y=train["VERTICAL_INTER_HRS"].values,trace=True,error_action="ignore",suppress_warnings=True)

model.fit(x=train["FLT_DATE"].values,y=train["VERTICAL_INTER_HRS"].values)

forecast = model.predict(n_periods=len(test))
forecast = pd.DataFrame(forecast,index=test.index,columns=["Prediciton"])

plt.plot(test["FLT_DATE"].values, np.array(forecast), color="blue")
plt.show()