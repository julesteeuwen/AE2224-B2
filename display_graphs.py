import csv
import matplotlib.pyplot as plt
import datetime
from preprocessing import cleanlist,ANSPs,split_data,get_data, read_data
from complexity_calculation import calculate_scores_daily, calculate_scores_monthly, calculate_scores_yearly



#service_provider = input("Enter air service provider")  #has to be an existing one, written exactly as in the data excel
def graphdata(data, ANSPName, indicator):
    # start_date = datetime.date(2014, 1, 1)
    # end_date = datetime.date(2016, 12, 31)
    # dates = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    
    while indicator not in ["1","2","3","4","5","6","7","8"]:
        indicator = input("Type your choice: ")
    if indicator == "1":
        indicator = 'VERTICAL_INTER_HRS'
        lable = ANSPName + ' Vertical Interactions'
        title = 'Vertical interactions with time'
    elif indicator == "2":
        indicator = 'HORIZ_INTER_HRS'
        lable = ANSPName + ' Horizontal Interactions'
        title = 'Horizontal interactions with time' 
    elif indicator == "3":
        indicator = 'SPEED_INTER_HRS'
        lable = ANSPName + ' Speed Interactions'
        title = 'Speed interactions with time' 
    elif indicator == "4":
        indicator = 'Vertical_score'
        lable = ANSPName + ' Vertical Score'
        title = 'Vertical interaction scores with time' 
    elif indicator == "5":
        indicator = 'Horizontal_score'
        lable = ANSPName + ' Horizontal Score'
        title = 'Horizontal interaction scores with time' 
    elif indicator == "6":
        indicator = 'Speed_score'
        lable = ANSPName + ' Speed Score'
        title = 'Speed interaction scores with time' 
    elif indicator == "7":
        indicator = 'Complexity_score'
        lable = ANSPName + ' Complexity Score'
        title = 'Complexity score with time' 
    elif indicator == "8":
        indicator = 'Adjusted_density'
        lable = ANSPName + ' Adjusted Density'
        title = 'Adjusted density with time' 


    #filename = 'datasets/split_2014-2016.csv'  # Change this to the path of your CSV file
    #column_data = read_csv_column(filename, choice, service_provider)
    column_data = data[indicator]
    column_data.plot(label = lable)
    plt.xlabel('Time')
    #plt.title(title)
    plt.legend()
    
    



def graphmultipledata(SelectedANSPs, ANSPsdf, ANSPs, choice):
     

    for indicator in choice:
        for ANSPName in SelectedANSPs:
            data, ANSPName = get_data(ANSPName, ANSPsdf, ANSPs)

            #data = calculate_scores_daily(data)
            data = calculate_scores_monthly(data)
            #data = calculate_scores_yearly(data)

            graphdata(data, ANSPName, indicator)

    plt.ylim(0)
    plt.show()


def displaygraphs(ANSPsdf, ANSPs):
    
    SelectedANSPs = input("Which ANSPs would you want data from? (separate ANSPs by comma) ")

    SelectedANSPs = [x.strip() for x in SelectedANSPs.split(',')]


    
    print("For vertical interactions hours \"1\" and then press ENTER")
    print("For horisontal interactions hours \"2\" and then press ENTER")
    print("For speed interactions hours \"3\" and then press ENTER")
    print("For vertical interactions score \"4\" and then press ENTER")
    print("For horizontal interactions score \"5\" and then press ENTER")
    print("For speed interactions score \"6\" and then press ENTER")
    print("For complexity score \"7\" and then press ENTER")
    print("For adjusted density \"8\" and then press ENTER")
    choice = input("Type your choice (comma separated):")

    choice = [x.strip() for x in choice.split(',')]

    graphmultipledata(SelectedANSPs, ANSPsdf, ANSPs, choice)