import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from scipy.sparse import csr_matrix
import gzip
import json

# Phase 1: Data Preparation
# Step 1: Load the Traffic Flow Forecasting Dataset from the .mat File
import scipy.io
# Function to load and prepare the data
def load_and_prepare_data(mat_file_path):
    # Load the .mat file
    mat = scipy.io.loadmat(mat_file_path)
    # Extract training and testing data
    tra_X_tr = mat['tra_X_tr']
    tra_Y_tr = mat['tra_Y_tr']
    tra_X_te = mat['tra_X_te']
    tra_Y_te = mat['tra_Y_te']
    tra_adj_mat = mat['tra_adj_mat']
    # Save the data using pickle for later use
    with open('tra_X_tr.pkl', 'wb') as f:
        print(tra_X_tr)
        pickle.dump(tra_X_tr, f)
    with open('tra_Y_tr.pkl', 'wb') as f:
        print(tra_Y_tr)
        pickle.dump(tra_Y_tr, f)
    print("Data preparation complete. Data saved as pickle files.")
    
# Load and prepare the data
load_and_prepare_data('traffic_dataset.mat')