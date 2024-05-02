# calculates sensitivy of the models to the indicators
# import stuff
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

#set default parameters
file = 'Datasets/2017-2019.csv'
ansps = ['Skyguide', 'MUAC', 'DSNA']
# make new dataframes
def make_new_DFs(file=file,sensi_parameter = 0.9):
    dataframe = pd.read_csv(file, index_col= 'FLT_DATE',parse_dates=True, date_format='%d-%m-%Y',delimiter=';').dropna()
    new_df = dataframe.copy()
    new_df['VERTICAL_INTER_HRS'] *= sensi_parameter
    new_df.to_csv("Datasets/2017-2019_vertical_sensitivity.csv", index=True)

    new_df = dataframe.copy()
    new_df['HORIZ_INTER_HRS'] *= sensi_parameter
    new_df.to_csv("Datasets/2017-2019_horizontal_sensitivity.csv", index=True)

    new_df = dataframe.copy()
    new_df['SPEED_INTER_HRS'] *= sensi_parameter
    new_df.to_csv("Datasets/2017-2019_speed_sensitivity.csv", index=True)
make_new_DFs(file,0.9)

# calculate complexity score based on old dataframes
def calculate_actual_complexity(file, ansps):
    df = pd.read_csv(file, index_col= 'FLT_DATE',parse_dates=True, date_format='%d-%m-%Y',delimiter=';').dropna()
    df = df[df['ENTITY_NAME'].isin(ansps)]
    ansps = df['ENTITY_NAME'].unique()
    cplx = []
    for ansp in ansps:
        df_ansp = df[df['ENTITY_NAME'] == ansp]
        VERTICAL_INTER_HRS = sum(df_ansp['VERTICAL_INTER_HRS'])
        HORIZ_INTER_HRS = sum(df_ansp['HORIZ_INTER_HRS'])
        SPEED_INTER_HRS = sum(df_ansp['SPEED_INTER_HRS'])
        CPLX_FLIGHT_HRS = sum(df_ansp['CPLX_FLIGHT_HRS'])
        cplx_ansp = (VERTICAL_INTER_HRS + HORIZ_INTER_HRS + SPEED_INTER_HRS)*60 / CPLX_FLIGHT_HRS
        cplx.append(cplx_ansp)
    return cplx, ansps



# plot the results
def plot_achtual_complexity(file, ansps):
    cplx, ansps = calculate_actual_complexity(file, ansps)
    fig, ax = plt.subplots()
    bar_colors = ['tab:red', 'tab:blue', 'tab:green']
    ax.bar(ansps, cplx, color=bar_colors)
    ax.set_ylabel('Complexity score')
    plt.show()

def plot_change_actual_complexity(file, ansps):
    cplx_old, ansps = calculate_actual_complexity(file, ansps)
    cplx_verti, ansps = calculate_actual_complexity('Datasets/2017-2019_vertical_sensitivity.csv', ansps)
    cplx_hori, ansps = calculate_actual_complexity('Datasets/2017-2019_horizontal_sensitivity.csv', ansps)
    cplx_speed, ansps = calculate_actual_complexity('Datasets/2017-2019_speed_sensitivity.csv', ansps)
    change_verti = cplx_old - cplx_verti
    change_hori = cplx_old - cplx_hori
    change_speed = cplx_old - cplx_speed

    print(change_verti, change_hori, change_speed)

    ''''
    penguin_means = {
    'Bill Depth': (18.35, 18.43, 14.98),
    'Bill Length': (38.79, 48.83, 47.50),
    'Flipper Length': (189.95, 195.82, 217.19),
}
    x = np.arange(len(ansps))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in penguin_means.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Length (mm)')
    ax.set_title('Impact of interactions on existing complexity score')
    ax.set_xticks(x + width, species)
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, 250)

    plt.show()
    '''


def plot_new_complexity(file, ansps):
    cplx, ansps = calculate_actual_complexity(file, ansps)
    fig, ax = plt.subplots()
    bar_colors = ['tab:red', 'tab:blue', 'tab:green']
    ax.bar(ansps, cplx, color=bar_colors)
    ax.set_ylabel('Complexity score')
    plt.show()

#execute the functions
plot_change_actual_complexity(file, ansps)