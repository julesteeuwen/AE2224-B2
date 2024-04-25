from preprocessing import *
from read_from_file import *
from MultipleSeasonality import *
from complexity_calculation import calculate_scores_daily, calculate_scores_monthly, calculate_scores_yearly
from AUTO_ARIMA import auto_ARIMA

mutlipleseason = True

TrafficData1 = read_data("Datasets/split_2014-2016.csv") #Change to choose CSV file

ANSPs = ANSPs(TrafficData1)
ANSPs = cleanlist(ANSPs)
ANSPsdf = split_data(TrafficData1, ANSPs)
ANSPName = input("Which ANSP would you want data from?")
data, ANSPName = get_data(ANSPName, ANSPsdf, ANSPs)

print(data)
# data = calculate_scores_daily(data)
# auto_ARIMA(data,"Complexity_score",plotting=True)
if mutlipleseason:
    TrafficData2 = readfilemultipleseason("Datasets/split_2014-2016.csv")
    ANSPsdf = split_data(TrafficData2, ANSPs)
    ANSPName = input("Which ANSP would you want data from?")
    data, ANSPName = get_data(ANSPName, ANSPsdf, ANSPs)
    df = data[["FLT_DATE", "VERTICAL_INTER_HRS"]]
    df.insert(0, 'unique_id', 'HRS')
    df.tail() 
    df = df.rename(columns={"FLT_DATE":'ds',"VERTICAL_INTER_HRS":'y' })
    print(df)
    MultipleSeasonalityDecomp(df, 20)
    # yearly_seasonality_check(data["VERITCAL_INTER_HRS"])