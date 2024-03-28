import csv
import matplotlib.pyplot as plt
import datetime

from preprocessing import cleanlist,ANSPs,split_data,get_data, read_data
from complexity_calculation import calculate_scores_daily, calculate_scores_monthly, calculate_scores_yearly

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






    