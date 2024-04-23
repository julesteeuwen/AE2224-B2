from preprocessing import *
from archive.read_from_file import *
from preprocessing.complexity_calculation import calculate_scores_daily, calculate_scores_monthly, calculate_scores_yearly



TrafficData1 = read_data("Datasets/split_2014-2016.csv") #Change to choose CSV file

ANSPs = ANSPs(TrafficData1)
ANSPs = cleanlist(ANSPs)
ANSPsdf = split_data(TrafficData1, ANSPs)
ANSPName = input("Which ANSP would you want data from?")
data, ANSPName = get_data(ANSPName, ANSPsdf, ANSPs)


data = calculate_scores_daily(data)
