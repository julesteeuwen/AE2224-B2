from preprocessing import *
from complexity_calculation import calculate_scores_daily, calculate_scores_monthly, calculate_scores_yearly



TrafficData1 = read_data("Datasets/split_2014-2016.csv")
SortedData = sort_data(TrafficData1)

ANSPs = ANSPs(SortedData)
ANSPs = cleanlist(ANSPs)
ANSPsdf = split_data(SortedData, ANSPs)
ANSPName = input("Which ANSP would you want data from?")
data = get_data(ANSPName, ANSPsdf, ANSPs)


#data = calculate_scores_daily(data)
#data = calculate_scores_monthly(data)
data = calculate_scores_yearly(data)


print(data)


