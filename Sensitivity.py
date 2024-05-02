# calculates sensitivy of the models to the indicators
# import stuff
import pandas as pd
import csv
import matplotlib.pyplot as plt

#set default parameters
file = 'Datasets/2017-2019.csv'
ansps = ['Skyguide', 'MUAC', 'DSNA']
# make new dataframes
def make_new_DFs(file,sensi_parameter = 0.9):
    dataframe = pd.read_csv(file, index_col= 'FLT_DATE',parse_dates=True, date_format='%d-%m-%Y',delimiter=';').dropna()
    dataframe_vert = dataframe['VERTICAL_INTER_HRS']*sensi_parameter
    dataframe_hori = dataframe['HORIZ_INTER_HRS']*sensi_parameter
    dataframe_speed = dataframe['SPEED_INTER_HRS']*sensi_parameter
    dataframe_vert.to_csv('Datasets/2017-2019_sens_vert.csv', sep='\t')
    dataframe_hori.to_csv('Datasets/2017-2019_sens_hori.csv', sep='\t')
    dataframe_speed.to_csv('Datasets/2017-2019_sens_speed.csv', sep='\t')
 
# calculate complexity score based on old dataframes
def calculate_old_complexity(file, ansps):
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

# calculate complexity score based on new dataframes
def calculate_new_complexity(file, ansps):
    cplx = 0

    return cplx,  ansps


# plot the results
def plot_old_complexity(file, ansps):
    cplx, ansps = calculate_old_complexity(file, ansps)
    fig, ax = plt.subplots()
    bar_colors = ['tab:red', 'tab:blue', 'tab:green']
    ax.bar(ansps, cplx, color=bar_colors)
    ax.set_ylabel('Complexity score')
    plt.show()

def plot_new_complexity(file, ansps):
    cplx, ansps = calculate_new_complexity(file, ansps)
    fig, ax = plt.subplots()
    bar_colors = ['tab:red', 'tab:blue', 'tab:green']
    ax.bar(ansps, cplx, color=bar_colors)
    ax.set_ylabel('Complexity score')
    plt.show()

#execute the functions