from preprocessing import *
from read_from_file import *
from complexity_calculation import calculate_scores_daily, calculate_scores_monthly, calculate_scores_yearly



TrafficData1 = read_data("Datasets/split_2014-2016.csv") #Change to choose CSV file

ANSPs = ANSPs(TrafficData1)
ANSPs = cleanlist(ANSPs)
print(ANSPs)
ANSPsdf = split_data(TrafficData1, ANSPs)
ANSPName = input("Which ANSP would you want data from? ")
data, ANSPName = get_data(ANSPName, ANSPsdf, ANSPs)



#data = calculate_scores_daily(data)
data = calculate_scores_monthly(data)
#data = calculate_scores_yearly(data)


#print(data)

graphdata(data, ANSPName)
