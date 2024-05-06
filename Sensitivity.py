# calculates sensitivy of the models to the indicators
# import stuff
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

#set default parameters
file = 'Datasets/split_2017-2019.csv'
ansps = ['Skyguide', 'MUAC', 'DSNA']
# make new dataframes
def make_new_DFs(file=file, sensi_parameter = 0.9):
    dataframe = pd.read_csv(file,parse_dates=True, index_col= 'YEAR', date_format='%d-%m-%Y',delimiter=',').dropna()
    new_df = dataframe.copy()
    new_df['VERTICAL_INTER_HRS'] *= sensi_parameter
    new_df.to_csv("Datasets/2017-2019_vertical_sensitivity.csv", index=False)

    new_df = dataframe.copy()
    new_df['HORIZ_INTER_HRS'] *= sensi_parameter
    new_df.to_csv("Datasets/2017-2019_horizontal_sensitivity.csv", index=False)

    new_df = dataframe.copy()
    new_df['SPEED_INTER_HRS'] *= sensi_parameter
    new_df.to_csv("Datasets/2017-2019_speed_sensitivity.csv", index=False)
#make_new_DFs(file,0.9)

# calculate complexity score based on old dataframes
def calculate_actual_complexity(file, ansps):
    df = pd.read_csv(file, index_col= 'FLT_DATE',parse_dates=True, date_format='%d-%m-%Y',delimiter=',').dropna()
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
    change_verti = []
    change_hori = []
    change_speed = []
    for i in range(len(cplx_old)):
        change_verti.append(abs((cplx_verti[i] - cplx_old[i])/cplx_old[i])*100)
        change_hori.append(abs((cplx_hori[i] - cplx_old[i])/cplx_old[i])*100)
        change_speed.append(abs((cplx_speed[i] - cplx_old[i])/cplx_old[i])*100)

    print(change_verti, change_hori, change_speed)
    # set width of bar 
    barWidth = 0.25
    fig = plt.subplots(figsize =(12, 8)) 
 
    # Set position of bar on X axis 
    br1 = np.arange(len(change_verti)) 
    br2 = [x + barWidth for x in br1] 
    br3 = [x + barWidth for x in br2] 
 
    # Make the plot
    plt.bar(br1, change_verti, color = 'tab:orange', width = barWidth, edgecolor ='grey', label ='Vertical Interactions') 
    plt.bar(br2, change_hori, color ='tab:green', width = barWidth, edgecolor ='grey', label ='Horizontal Interactions') 
    plt.bar(br3, change_speed, color ='tab:blue', width = barWidth, edgecolor ='grey', label ='Speed Interactions') 
 
    # Adding Xticks 
    plt.ylabel('Complexity score change(%)', fontweight ='bold', fontsize = 15) 
    plt.xticks([r + barWidth for r in range(len(change_verti))], ansps)
 
    legend = plt.legend(loc='lower center', shadow=True, fancybox=True,bbox_to_anchor=(0.5, -0.3))

    #plt.setp(legend.get_title(), fontsize=30)
    plt.setp(legend.get_texts(), fontsize=25)
    plt.tight_layout()
    #plt.legend()
    plt.show() 

    

#execute the functions
plot_change_actual_complexity(file, ansps)