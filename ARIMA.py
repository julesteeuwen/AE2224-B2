import pandas as pd
import pmdarima as pmd
import matplotlib.pyplot as plt
import numpy as np
import sklearn as sk

#read file and and chosse parameters to predict
data = pd.read_csv('Datasets/AAPL.csv')
Predictor = data['Open']
Time = data['Date']

#reshape dataframe to numpy array
x = Time.to_numpy()
y = data['Close'].to_numpy()
array = np.arange(len(x)).reshape(-1, 1)
#print(array)

#train model
model = sk.linear_model.LinearRegression().fit(array, y)
Predicted_Predictor = model.predict(array)

# plot model
def plotting(x, y, xlabel, ylabel, title):
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.plot(array, Predicted_Predictor, color='red')
    plt.show()

plotting(Time, Predictor, 'Date', 'Close', 'AAPL Stock Price')
