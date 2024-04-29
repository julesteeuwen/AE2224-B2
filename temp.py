import pandas as pd
from sklearn.metrics import mean_squared_error as mse
from sktime.utils.plotting import plot_series
import matplotlib.pyplot as plt

train = pd.read_pickle('train.pkl')
test = pd.read_pickle('test.pkl')
predicted_values = pd.read_pickle('predicted.pkl')

# Calculate MSE
MSE = mse(test, predicted_values)

print(f"MSE: {MSE}")

# Plot the prediction
# plot_series(train, test, predicted_values, labels=['Train', 'Test', 'Predicted'])
plt.show()