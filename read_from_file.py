import csv

def read_csv_column(filename, column_index):
    x = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            try:
                value = float(row[column_index])
                x.append(value)
            except (IndexError, ValueError):
                # Handle cases where the row or cell is invalid
                pass
    return x

# Example usage
column_index = int(input("Enter the column index (0-based): "))
filename = 'datasets/split_2014-2016.csv'  # Change this to the path of your CSV file
column_data = read_csv_column(filename, column_index)
print("Column data:", column_data)