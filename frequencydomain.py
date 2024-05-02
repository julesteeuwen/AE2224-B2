from display_graphs import displaygraphs, plot_entire_dataset, plot_by_ANSP
from preprocessing import cleanlist,ANSPs,split_data,get_data, read_data
from complexity_calculation import calculate_scores_daily, calculate_scores_monthly, calculate_scores_yearly, total_complexity_by_ANSP, calculate_scores_weekly
from EWMA import plot_decompose
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

TrafficData1 = read_data("Datasets/split_2017-2019.csv")

df = calculate_scores_daily(TrafficData1)

df = df.dropna()

grouped = df.groupby('ENTITY_NAME')

# Extract one of the groups, for example, the first group

selected_group = grouped.get_group('ANS CR')

data = selected_group['Complexity_score']

# plot_decompose(data)

mean = np.mean(data)

data = data - mean

window_size = 365


# Calculate the moving average
#data = data.rolling(window=window_size, min_periods=window_size).mean()
data = data.dropna()


# Assuming df is your DataFrame and 'column_name' is the name of the column you want to plot
# Extract the data from the column


# Plotting in Time Domain
plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(data)
plt.title('Signal in Time Domain')
plt.xlabel('Time')
plt.ylabel('Amplitude')

# Plotting in Frequency Domain
plt.subplot(2, 1, 2)
# Compute the Fast Fourier Transform (FFT)
fft_result = np.fft.fft(data)

# Compute the frequencies corresponding to the FFT result
frequencies = np.fft.fftfreq(len(data))
frequencies = frequencies[np.abs(fft_result)>100]
fft_result = fft_result[np.abs(fft_result)>100]

# Plot the frequency spectrum
plt.scatter(frequencies, np.abs(fft_result))
plt.title('Frequency Spectrum')
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.xlim(left = 0)  # Show only positive frequencies (up to Nyquist frequency)
#plt.yscale('log')
plt.tight_layout()
plt.show()




