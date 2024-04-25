import numpy as np
import torch
from matplotlib import pyplot as plt
from scipy import signal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.model_selection import train_test_split

#model parameters:
thing_to_predict = 'CPLX_INTER'
ANSP = 'Skyguide'
n_hidden_neurons = 30
learning_rate = 1e-1
n_epochs = 3000

# Set the PyTorch and numpy random seeds for reproducibility:
seed = 0
torch.manual_seed(seed)
np.random.seed(seed)


def load_actual_data():
    df = pd.read_csv('Datasets/split_2017-2019.csv', index_col='FLT_DATE', parse_dates=True, date_format='%d-%m-%Y')
    df.dropna(inplace=True)

    # Filtering data and selecting an ANSP
    df_vert = df.loc[:, thing_to_predict].to_frame()
    df_ansp = df_vert.loc[df['ENTITY_NAME'] == ANSP].copy()
    df_ansp.index.freq = pd.infer_freq(df_ansp.index)


    # Split data
    slice = int(0.8*len(df_ansp))
    train_ansp = df_ansp[:slice]
    test_ansp = df_ansp[slice:]
    
    #put in right shape
    y_train = train_ansp[thing_to_predict].to_numpy()
    x_train = np.linspace(1, len(y_train), len(y_train))
    x_train = x_train.reshape(len(y_train), 1)
    y_train = y_train.reshape(len(y_train), 1)
    y_test = test_ansp[thing_to_predict].to_numpy()
    x_test = np.linspace(1, len(y_test), len(y_test))
    x_test = x_test.reshape(len(y_test), 1)
    y_test = y_test.reshape(len(y_test), 1)
    return(x_train,y_train, x_test, y_test)

def train_regressor_nn(n_features, n_hidden_neurons, learning_rate, n_epochs, X, Y):
    # Define the model:
    model = torch.nn.Sequential(torch.nn.Linear(n_features, n_hidden_neurons),
                            torch.nn.Sigmoid(),torch.nn.Linear(n_hidden_neurons, n_hidden_neurons), torch.nn.Sigmoid(),torch.nn.Linear(n_hidden_neurons, 1))

    # MSE loss function:
    loss_fn = torch.nn.MSELoss()

    # optimizer:
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
    # Train the network:
    for t in range(n_epochs):

        y_pred = model(X)

        loss = loss_fn(y_pred, Y)
        if t % 100 == 0:
            print(t, loss.item())

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # return the trained model
    return model


[X_train, Y_train, X_test,Y_test] = load_actual_data()


#standardize data
X_train = (X_train - np.mean(X_train))/np.std(X_train)
Y_train = (Y_train - np.mean(Y_train))/np.std(Y_train)
X_test = (X_test - np.mean(X_test))/np.std(X_test)
Y_test = (Y_test - np.mean(Y_test))/np.std(Y_test)

# Convert to torch tensors:
X_train = torch.from_numpy(X_train).float()
Y_train = torch.from_numpy(Y_train).float()
X_test = torch.from_numpy(X_test).float()
Y_test = torch.from_numpy(Y_test).float()


#define model
model = train_regressor_nn(X_train.shape[1], n_hidden_neurons, learning_rate, n_epochs, X_train, Y_train)

# Predict the output for the test set:
y_pred = model(X_test)

# Convert the torch tensors to numpy arrays:
y_pred = y_pred.detach().numpy()
y_test = Y_test.detach().numpy()

# Plot the predicted Y vs the real Y:
plt.plot(y_test, label='Real Y')
plt.plot(y_pred, label='Predicted Y')
plt.xlabel('Time')
plt.ylabel('Y')
plt.legend()
plt.show()
print('Root Mean Squared Error: ', np.sqrt(np.mean((y_pred - y_plot)**2)))
