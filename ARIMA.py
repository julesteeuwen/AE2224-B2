import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('Datasets/AAPL.csv')


def plotting(x, y, xlabel, ylabel, title):
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

plotting(data['Date'], data['Close'], 'Date', 'Close', 'AAPL Stock Price')
