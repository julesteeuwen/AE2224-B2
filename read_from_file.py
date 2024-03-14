import csv
import matplotlib.pyplot as plt
import datetime
import pandas as pd

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

start_date = datetime.date(2014, 1, 1)
end_date = datetime.date(2016, 12, 31)
dates = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]



service_provider = input("Enter air service provider")  #has to be an existing one, written exactly as in the data excel
print("For vertical interactions type \"1\" and then press ENTER")
print("For horisontal interactions type \"2\" and then press ENTER")
print("For speed interactions type \"3\" and then press ENTER")
choice = input("Type your choice:")
while choice not in ["1","2","3"]:
    choice = input("Type your choice:")
if choice == "1":
    choice = 8
elif choice == "2":
    choice = 9
else:
    choice = 10

filename = 'datasets/split_2014-2016.csv'  # Change this to the path of your CSV file
column_data = read_csv_column(filename, choice, service_provider)
print(column_data)
plt.plot(dates,column_data)
plt.xlabel('Time')
plt.ylabel('Vertical_interactions')
plt.title('Test')
plt.show()