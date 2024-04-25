import torch
import numpy as np
from preprocessing import *


#For reproducibility
seed = 0
torch.manual_seed(seed)
np.random.seed(seed)


#Import data
TrafficData1 = read_data("Datasets/split_2014-2016.csv") #Change to choose CSV file
SortedData = sort_data(TrafficData1)
SortedData = SortedData.dropna()
print(SortedData)
ANSPs = ANSPs(SortedData)
ANSPs = cleanlist(ANSPs)
ANSPsdf = split_data(SortedData, ANSPs)
ANSPName = input("Which ANSP would you want data from?")
data, ANSPName = get_data(ANSPName, ANSPsdf, ANSPs)



#Turn data into tensor


# n_features = 