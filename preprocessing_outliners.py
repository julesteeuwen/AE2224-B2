# importing libraries
import pandas as pd
import scipy
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt


# Load the dataset
df = pd.read_csv('split_2014-2016.csv', nrows = 5)
print(df.head())  ### print the first 5 rows of the data


#df.info()   ### check the null data
#df.isnull().sum()    ### calculates the number of missing values (NaN) in each column of the DataFrame
df.describe()   ### statistical summary of the dataframe


# Box Plots
fig, axs = plt.subplots(4,1,dpi=95, figsize=(7,17))
i = 0
for col in df.columns:
	axs[i].boxplot(df[col], vert=False)
	axs[i].set_ylabel(col)
	i+=1
plt.show()


# Identify the quartiles
q1, q3 = np.percentile(df['CPLX_INTER'], [25, 75])
# Calculate the interquartile range
iqr = q3 - q1
# Calculate the lower and upper bounds
lower_bound = q1 - (1.5 * iqr)
upper_bound = q3 + (1.5 * iqr)
# Drop the outliers
clean_data = df[(df['CPLX_INTER'] >= lower_bound) 
				& (df['CPLX_INTER'] <= upper_bound)]


# Identify the quartiles
q1, q3 = np.percentile(clean_data['VERTICAL_INTER_HRS'], [25, 75])
# Calculate the interquartile range
iqr = q3 - q1
# Calculate the lower and upper bounds
lower_bound = q1 - (1.5 * iqr)
upper_bound = q3 + (1.5 * iqr)
# Drop the outliers
clean_data = clean_data[(clean_data['VERTICAL_INTER_HRS'] >= lower_bound) 
						& (clean_data['VERTICAL_INTER_HRS'] <= upper_bound)]


# Identify the quartiles
q1, q3 = np.percentile(clean_data['HORIZ_INTER_HRS'], [25, 75])
# Calculate the interquartile range
iqr = q3 - q1
# Calculate the lower and upper bounds
lower_bound = q1 - (1.5 * iqr)
upper_bound = q3 + (1.5 * iqr)
# Drop the outliers
clean_data = clean_data[(clean_data['HORIZ_INTER_HRS'] >= lower_bound) 
						& (clean_data['HORIZ_INTER_HRS'] <= upper_bound)]


# Identify the quartiles
q1, q3 = np.percentile(clean_data['SPEED_INTER_HRS'], [25, 75])
# Calculate the interquartile range
iqr = q3 - q1
# Calculate the lower and upper bounds
lower_bound = q1 - (1.5 * iqr)
upper_bound = q3 + (1.5 * iqr)
# Drop the outliers
clean_data = clean_data[(clean_data['SPEED_INTER_HRS'] >= lower_bound) 
						& (clean_data['SPEED_INTER_HRS'] <= upper_bound)]



