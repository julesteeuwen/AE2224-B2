import torch
from matplotlib import pyplot as plt
import numpy as np
import random
import pandas as pd
from sklearn.model_selection import train_test_split

#Model parameters
n_hidden_neurons = 10
learning_rate = 1e-2
n_epochs = 100
show_plot = False
stop_when_val_error_increases = False
np.set_printoptions(threshold = np.inf)



# Load the data and split it into separate pieces
dataframe = pd.read_csv('Datasets/2017-2019.csv', index_col= 'FLT_DATE',parse_dates=True, date_format='%d-%m-%Y',delimiter=';')
dataframe = dataframe.dropna()  # drop missing values
df1 = dataframe[dataframe['ENTITY_NAME'] == 'LVNL']
field = 'CPLX_INTER'
data = df1[field].values
train, test_val = train_test_split(df1[field], train_size=0.7)
test, val = train_test_split(test_val, train_size=0.5)

print(df1.index.day.values)

x_training = train.index
#print(x_training)
y_training = train.values
x_test = 0
y_test = test.values
x_val = 0
y_val = val.values

"""
# Model
model = torch.nn.Sequential(torch.nn.Linear(3, n_hidden_neurons),
                            torch.nn.Sigmoid(),torch.nn.Linear(n_hidden_neurons, 1))

#Loss function
loss_fn = torch.nn.MSELoss(reduction='sum')

# optimizer
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# initialize variables
training_loss = np.zeros(n_epochs)
validation_loss = np.zeros(n_epochs)

for t in range(n_epochs):
    y_pred = model(x_training)
    loss = loss_fn(y_pred, y_training)
    if t % 100 == 0:
        print(t, loss.item())
    training_loss[t] = loss.item()

    # Backpropagation
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # Determine validation loss
    y_val_pred = model(x_val)
    val_loss = loss_fn(y_val_pred, y_val)
    validation_loss[t] = val_loss.item()


# Get losses
y_pred = model(x_training)
loss = loss_fn(y_pred, y_training)
print(f'Average loss on the training set: {loss.item()/n_training:.2f}')

y_pred = model(x_val)
loss = loss_fn(y_pred, y_val)
print(f'Average loss on the validation set: {loss.item()/n_val:.2f}')

y_pred = model(x_test)
loss = loss_fn(y_pred, y_test)
print(f'Average loss on the test set: {loss.item()/n_test:.2f}')
"""
