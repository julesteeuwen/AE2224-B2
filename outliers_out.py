from preprocessing import read_data
from matplotlib import pyplot as plt



data = read_data("Datasets/split_2017-2019.csv")

import pandas as pd

def apply_moving_average(df, window_size=183, perc=30):
    # Calculate moving average
    df['Moving_Avg'] = df['VERTICAL_INTER_HRS'].rolling(window=window_size, min_periods=1).mean()
    
    # Remove data points more than 20% higher than the moving average
    df['Is_Outlier'] = df['VERTICAL_INTER_HRS'] > (1+perc/100) * df['Moving_Avg']
    df = df[~df['Is_Outlier']]
    
    # Drop temporary columns
    df = df.drop(columns=['Moving_Avg', 'Is_Outlier'])
    
    return df

'''
df1 = data[data['ENTITY_NAME'] == 'LVNL']
result = apply_moving_average(df1)

plt.plot(df1["VERTICAL_INTER_HRS"], color='red')
plt.plot(result["VERTICAL_INTER_HRS"], color='blue')
plt.show()'
'''
