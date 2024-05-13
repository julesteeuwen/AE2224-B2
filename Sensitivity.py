# calculates sensitivy of the models to the indicators
# import stuff
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from MultipleSeasonality import predict_ansp_TBATS

#set default parameters
file = 'Datasets/split_2017-2019.csv'
ansps = ['Skyguide', 'MUAC', 'DSNA']
n = 274
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
def calculate_actual_complexity(file, ansps, plotting = True):
    df = pd.read_csv(file, index_col= 'FLT_DATE',parse_dates=True, date_format='%d-%m-%Y',delimiter=',').dropna()
    df = df[df['ENTITY_NAME'].isin(ansps)]
    ansps = df['ENTITY_NAME'].unique()
    cplx = []
    if plotting:
        for ansp in ansps:
            df_ansp = df[df['ENTITY_NAME'] == ansp]
            VERTICAL_INTER_HRS = sum(df_ansp['VERTICAL_INTER_HRS'])
            HORIZ_INTER_HRS = sum(df_ansp['HORIZ_INTER_HRS'])
            SPEED_INTER_HRS = sum(df_ansp['SPEED_INTER_HRS'])
            CPLX_FLIGHT_HRS = sum(df_ansp['CPLX_FLIGHT_HRS'])
            cplx_ansp = (VERTICAL_INTER_HRS + HORIZ_INTER_HRS + SPEED_INTER_HRS)*60 / CPLX_FLIGHT_HRS
            cplx.append(cplx_ansp)
    else:
        df = df[df['ENTITY_NAME'] == 'Skyguide']
        VERTICAL_INTER_HRS = df['VERTICAL_INTER_HRS']
        HORIZ_INTER_HRS = df['HORIZ_INTER_HRS']
        SPEED_INTER_HRS = df['SPEED_INTER_HRS']
        CPLX_FLIGHT_HRS = df['CPLX_FLIGHT_HRS']
        CPLX_INTER = df['CPLX_INTER']
        Adj_Density = CPLX_INTER*60 / CPLX_FLIGHT_HRS
        Struc_Index = (VERTICAL_INTER_HRS + HORIZ_INTER_HRS + SPEED_INTER_HRS) / CPLX_INTER
        cplx_ansp = (VERTICAL_INTER_HRS + HORIZ_INTER_HRS + SPEED_INTER_HRS)*60 / CPLX_FLIGHT_HRS

        plt.plot(df.index, cplx_ansp, color = 'tab:blue')  # Line plot
        #plt.plot(df.index, Adj_Density, label = 'Adjusted density', color = 'tab:green')
        #plt.plot(df.index, Struc_Index, label = 'Structural index', color = 'tab:blue')
        plt.ylabel('score')  # Y-axis label
        plt.xlabel('Date')  # X-axis label
        plt.legend()  # Show legend
        plt.xticks(rotation=45)
        plt.show()

    return cplx, ansps

def calculate_predicted_complexity(ansps, n ):
    test = predict_ansp_TBATS('Skyguide', 'HORIZ_INTER_HRS' ,n)
    print(test)




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
calculate_predicted_complexity('skyguide',n)
