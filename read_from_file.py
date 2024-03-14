import csv
import matplotlib.pyplot as plt
import datetime

def read_csv_column(filename, column_index, service_provider):
    x = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[4] == service_provider:
                try:
                    value = float(row[column_index])
                    x.append(value)
                except (IndexError, ValueError):
                    # Handle cases where the row or cell is invalid
                    pass
    return x

# construct the time axis in "dates"
# Example usage 8





#service_provider = input("Enter air service provider")  #has to be an existing one, written exactly as in the data excel
def graphdata(data, ANSPName):
    # start_date = datetime.date(2014, 1, 1)
    # end_date = datetime.date(2016, 12, 31)
    # dates = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    print("For vertical interactions hours \"1\" and then press ENTER")
    print("For horisontal interactions hours \"2\" and then press ENTER")
    print("For speed interactions hours \"3\" and then press ENTER")
    print("For vertical interactions score \"4\" and then press ENTER")
    print("For horizontal interactions score \"5\" and then press ENTER")
    print("For speed interactions score \"6\" and then press ENTER")
    print("For complexity score \"7\" and then press ENTER")
    print("For adjusted density \"8\" and then press ENTER")
    choice = input("Type your choice:")
    while choice not in ["1","2","3","4","5","6","7","8"]:
        choice = input("Type your choice:")
    if choice == "1":
        choice = 'VERTICAL_INTER_HRS'
        lable = 'Vertical Interactions'
        title = ANSPName + ' vertical interactions with time'
    elif choice == "2":
        choice = 'HORIZ_INTER_HRS'
        lable = 'Horizontal Interactions'
        title = ANSPName + ' horizontal interactions with time' 
    elif choice == "3":
        choice = 'SPEED_INTER_HRS'
        lable = 'Speed Interactions'
        title = ANSPName + ' speed interactions with time' 
    elif choice == "4":
        choice = 'Vertical_score'
        lable = 'Vertical Score'
        title = ANSPName + ' vertical interaction scores with time' 
    elif choice == "5":
        choice = 'Horizontal_score'
        lable = 'Horizontal Score'
        title = ANSPName + ' horizontal interaction scores with time' 
    elif choice == "6":
        choice = 'Speed_score'
        lable = 'Speed Score'
        title = ANSPName + ' speed interaction scores with time' 
    elif choice == "7":
        choice = 'Complexity_score'
        lable = 'Complexity Score'
        title = ANSPName + ' complexity score with time' 
    elif choice == "8":
        choice = 'Adjusted_density'
        lable = 'Adjusted Density'
        title = ANSPName + ' ajusted density with time' 


    #filename = 'datasets/split_2014-2016.csv'  # Change this to the path of your CSV file
    #column_data = read_csv_column(filename, choice, service_provider)
    column_data = data[choice]
    column_data.plot()
    plt.xlabel('Time')
    plt.ylabel(lable)
    plt.title(title)
    plt.show()