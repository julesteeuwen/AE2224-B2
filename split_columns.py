import csv

def split_csv(filename):
    new_rows = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            # Splitting the first column by ";"
            split_values = row[0].split(';')
            new_rows.append(split_values)
    return new_rows

def write_csv(filename, data):
    with open(filename, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(data)

# Example usage
filename = 'datasets/2014-2016.csv'  # Replace this with the path to your CSV file
new_data = split_csv(filename)
new_filename = 'datasets/split_2014-2016.csv'  # Choose a name for the new CSV file
write_csv(new_filename, new_data)
print(f"Data from '{filename}' has been split and written to '{new_filename}'.")
