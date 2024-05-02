import csv
import matplotlib.pyplot as plt
import datetime
import math
import numpy as np

from preprocessing import cleanlist,ANSPs,split_data,get_data, read_data
from complexity_calculation import calculate_scores_daily, calculate_scores_monthly, calculate_scores_yearly, total_complexity_by_ANSP, calculate_scores_weekly

    
    


def displaygraphs(ANSPsdf, ANSPs, period):
    #Displays graphs of multiple ANSPs for multiple indicators
    
    SelectedANSPs = input("Which ANSPs would you want data from? (separate ANSPs by comma) ")

    SelectedANSPs = [x.strip() for x in SelectedANSPs.split(',')]


    choice = select_columns()

    graph_info = convert_choice(choice)
    


    fig, axs = plt.subplots(nrows = len(graph_info), sharex='col')
    
     
    

    for i in range(len(graph_info)):
        
        labels = [0]*len(graph_info)
        
        for ANSPName in SelectedANSPs:
            data, ANSPName = get_data(ANSPName, ANSPsdf, ANSPs)
            
            if period == 'day':
                data = calculate_scores_daily(data)
            elif period == 'month':
                data = calculate_scores_monthly(data)
            elif period == 'year':
                data = calculate_scores_yearly(data)
            elif period == 'week':
                data = calculate_scores_weekly(data)
            else:
                print('invalid period')
                break

            

            labels[i] = ANSPName
            #filename = 'datasets/split_2014-2016.csv'  # Change this to the path of your CSV file
            #column_data = read_csv_column(filename, choice, service_provider)
            column_data = data[graph_info[i][0]]
            
            column_data.plot(ax = axs[i], label = labels[i])
            axs[i].set_xlabel('Time')
            axs[i].set_title(graph_info[i][1])
            axs[i].grid()
            
        #axs[i].legend()
        axs[i].set_ylim(0)
        
        
    #handles, labels = axs.get_legend_handles_labels()
    handles, labels = plt.gca().get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right')        
    
    
    plt.show()


def plot_entire_dataset(data,period):
    # Plots indicators of choice for the total dataset on daily, monthly or yearly basis
    

    if period == 'day':
        data = calculate_scores_daily(data)
    elif period == 'month':
        data = calculate_scores_monthly(data)
    elif period == 'year':
        data = calculate_scores_yearly(data)
    elif period == 'week':
        data = calculate_scores_weekly(data)
    else:
        print('invalid period')
        

    choice = select_columns()

    graph_info = convert_choice(choice)

    fig, axs = plt.subplots(nrows = len(graph_info), sharex='col')


    for i in range(len(graph_info)):
        
        data[graph_info[i][0]].plot(ax = axs[i])
        
        axs[i].set_xlabel('Time')
        axs[i].set_title(graph_info[i][1])
        axs[i].grid()
            
        
        #axs[i].set_ylim(0)

    plt.show()
    


def select_columns():
    print("For vertical interactions hours \"1\" and then press ENTER")
    print("For horizontal interactions hours \"2\" and then press ENTER")
    print("For speed interactions hours \"3\" and then press ENTER")
    print("For vertical interactions score \"4\" and then press ENTER")
    print("For horizontal interactions score \"5\" and then press ENTER")
    print("For speed interactions score \"6\" and then press ENTER")
    print("For complexity score \"7\" and then press ENTER")
    print("For adjusted density \"8\" and then press ENTER")
    print("For structural index \"9\" and then press ENTER")
    print("For complexity flight hours \"10\" and then press ENTER")
    print("For complexity interaction hours \"11\" and then press ENTER")
    choice = input("Type your choice (comma separated):")

    choice = [x.strip() for x in choice.split(',')]

    return choice

def convert_choice(choice):
    graph_info = []

    for indicator in choice:
        if indicator == "1":
            indicator = 'VERTICAL_INTER_HRS'
            
            title = 'Vertical interaction hours'
        elif indicator == "2":
            indicator = 'HORIZ_INTER_HRS'
            
            title = 'Horizontal interaction hours' 
        elif indicator == "3":
            indicator = 'SPEED_INTER_HRS'
            
            title = 'Speed interaction hours' 
        elif indicator == "4":
            indicator = 'Vertical_score'
            
            title = 'Vertical interaction score' 
        elif indicator == "5":
            indicator = 'Horizontal_score'
            
            title = 'Horizontal interaction score' 
        elif indicator == "6":
            indicator = 'Speed_score'
            
            title = 'Speed interaction score' 
        elif indicator == "7":
            indicator = 'Complexity_score'
            
            title = 'Complexity score' 
        elif indicator == "8":
            indicator = 'Adjusted_density'
            
            title = 'Adjusted density' 
        elif indicator == "9":
            indicator = 'Structural_index'
            title = 'Structural index'

        elif indicator == "10":
            indicator = 'CPLX_FLIGHT_HRS'
            title = 'Complexity flight hours'

        elif indicator == "11":
            indicator = 'CPLX_INTER'
            title = 'Complexity interaction hours'

        graph_info.append([indicator, title])

    return graph_info


    
def plot_by_ANSP(data, vertsens = 1, hortsens = 1, speedsens = 1):
    #Plots selected indicators over the entire period by ANSP 

    data = total_complexity_by_ANSP(data, vertsens, hortsens, speedsens)
    choice = select_columns()
    graph_info = convert_choice(choice)
    
    # fig, axs = plt.subplots(nrows = len(graph_info), sharex='col')


    # for i in range(len(graph_info)):
        
    #     data[graph_info[i][0]].plot.bar(ax = axs[i])
        
    #     axs[i].set_xlabel('Time')
    #     axs[i].set_title(graph_info[i][1])
    #     axs[i].grid()

    x = np.arange(len(data))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for indicator, title in graph_info:
        offset = width * multiplier
        rects = ax.bar(x + offset, data[indicator], width, label=title)
        #ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    
    ax.set_title('Indicators by ANSP')
    ax.set_xticks(x + width, data.index, rotation=90)
    ax.legend(loc='upper left', ncols=3)
    ax.grid()
    

    plt.show()

    

    
    

