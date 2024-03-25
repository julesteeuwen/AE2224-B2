import matplotlib.pyplot as plt

from preprocessing import cleanlist,ANSPs,split_data,get_data, read_data
from display_graphs import displaygraphs, plot_entire_dataset, plot_by_ANSP
from complexity_calculation import calculate_scores_daily, calculate_scores_monthly, calculate_scores_yearly




TrafficData1 = read_data("Datasets/split_2017-2019.csv") #Change to choose CSV file



ANSPs = ANSPs(TrafficData1)
ANSPs = cleanlist(ANSPs)
ANSPsdf = split_data(TrafficData1, ANSPs)

#for plotting data selected 'day', 'month' or 'year'
#plot_entire_dataset(TrafficData1, 'month')
#displaygraphs(ANSPsdf, ANSPs, 'month')
#plot_by_ANSP(TrafficData1)

