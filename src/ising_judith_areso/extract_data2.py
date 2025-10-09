import numpy as np
import pandas as pd
import os
from  matplotlib import pyplot as plt

def extract_eggwin_txt(folder_path_eggwin):
    files = [f for f in os.listdir(folder_path_eggwin)]
    files.sort()
    data = {}
    for f in files:
        temperature = float(str(f).split("temp")[1].split(".txt")[0])
        file_path = os.path.join(folder_path_eggwin,f)
        df = pd.read_csv(file_path,delimiter=r"\s+",skiprows=1,header=None)
        df.columns = ["conf","E","M"]
        data[temperature] = df
    return data


def extract_beatrix_txt(folder_path_beatrix):
    files = [f for f in os.listdir(folder_path_beatrix)]
    files.sort()
    data = {}
    for f in files:
        temperature = float(str(f).split("T")[1].split(".txt")[0])
        file_path = os.path.join(folder_path_beatrix,f)
        df = pd.read_csv(file_path,delimiter=r"\s+",header=None)
        df.columns = ["conf","E","M"]
        data[temperature] = df
    return data

def extract_siegfried_txt(folder_path_siegfried):
    files = [f for f in os.listdir(folder_path_siegfried)]
    files.sort()
    data = {}
    for f in files:
        temperature = float(str(f).split("T")[1].split(".txt")[0])
        file_path = os.path.join(folder_path_siegfried,f)
        df = pd.read_csv(file_path,delimiter=r"\s+",usecols=[1,2,3],header=None)
        df.columns = ["conf","E","M"]
        data[temperature] = df
    return data

def check_number_of_columns(df):
    col_number = df.shape[1]
    return col_number

def plot_columns(col_number, df):
    x = df.iloc[:,0]
    y1 = df.iloc[:,1]
    y2 = df.iloc[:,2]
    plt.Figure()
    plt.plot(x,y1)
    plt.plot(x,y2)
    plt.show()

#def identify_columns(df,col_number):
#    for i in range(col_number):
#        if (df.iloc[:,i].nunique() == 1):
#            temp_col = df.iloc[:,i]
#        elif (df.iloc[:,i].diff().iloc[1:] == 1).all():
#            conf_col = df.iloc[:,i]
#        else:




folder_path_eggwin = os.path.join('..', '..', 'Ising2D/Eggwin/Ising_2D_MCMC_Ns8_Ns8')
folder_path_beatrix = os.path.join('..', '..', 'Ising2D/Beaktrix/ising2d_L16')
folder_path_siegfried = os.path.join('..', '..', 'Ising2D/Siegfried/two_dimensional_ising_model_markov_chain_monte_carlo_Sz32')
data_eggwin = extract_eggwin_txt(folder_path_eggwin)
data_beatrix = extract_beatrix_txt(folder_path_beatrix)
data_siegfried = extract_siegfried_txt(folder_path_siegfried)
#check_number_of_columns(data[0.5])
#plot_columns(3, data[6.5])
