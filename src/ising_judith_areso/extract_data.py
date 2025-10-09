import numpy as np
import pandas as pd
import os
from  matplotlib import pyplot as plt

flags =["Eggwin", "Beaktrix","Siegfried"]
def chicken_type(flag):
    if flag == "Eggwin":
        folderpath = os.path.join('..', '..', 'Ising2D/Eggwin/Ising_2D_MCMC_Ns8_Ns8')
        splitstring = "temp"
        skippedrows = 1
        usedcols    = [0,1,2]
    elif flag == "Beaktrix":
        folderpath = os.path.join('..', '..', 'Ising2D/Beaktrix/ising2d_L16')
        splitstring = "T"
        skippedrows = 0
        usedcols    = [0,1,2]
    elif flag == "Siegfried":
        folderpath = os.path.join('..', '..', 'Ising2D/Siegfried/two_dimensional_ising_model_markov_chain_monte_carlo_Sz32')
        splitstring = "T"
        skippedrows = 0
        usedcols    = [1,2,3]
    else:
        print("Choose available chicken")
    return folderpath, splitstring, skippedrows, usedcols

def extract_txt(flag):
    folderpath, splitstring, skippedrows, usedcols = chicken_type(flag)
    files = [f for f in os.listdir(folderpath)]
    files.sort()
    data = {}
    for f in files:
        temperature = float(str(f).split(splitstring)[1].split(".txt")[0]) # 
        file_path = os.path.join(folderpath,f) 
        df = pd.read_csv(file_path,delimiter=r"\s+",skiprows=skippedrows,usecols=usedcols,header=None)
        data[temperature] = df.dropna(axis=0)
    if flag =="Siegfried":
        swap_dummyA = data[2.27]
        swap_dummyB = data[3.2]
        data[2.27] = swap_dummyB
        data[3.2] = swap_dummyA
    return data

def check_number_of_columns(df):
    col_number = df.shape[1]
    return col_number


def calculate_magnetisation_density(vol,df,flag):
    if flag =="Eggwin":
        df.columns = ["conf","M","E"]
    else:
        df.columns = ["conf","E","M"]
    M = df["M"]
    absolute_average_mag = np.mean(abs(M))
    stdv_mag = np.std(M)
    if absolute_average_mag <= 1 :
        mag_dens = absolute_average_mag
    else:
        mag_dens = absolute_average_mag / vol
    return mag_dens, stdv_mag

def absolute_average_magnetisation_over_Temperature(flag,vol):
    data = extract_txt(flag)
    mag_dens_list, stdv_list = [],[]
    for df in data.values():
        mag_dens,stdv_mag = calculate_magnetisation_density(vol,df,flag)
        mag_dens_list.append(mag_dens)
        stdv_list.append(stdv_mag)
    temp_list = data.keys()
    return temp_list, mag_dens_list, stdv_list

def plot_abs_av_mgn_over_T(flag,vol):
    temp_list,mag_dens_list, stdv_list =absolute_average_magnetisation_over_Temperature(flag,vol) 
    plt.Figure()
    plt.plot(temp_list,mag_dens_list,label=f"L={vol}")


def average_energy_density(vol,df,flag):
    if flag =="Eggwin":
        df.columns = ["conf","M","E"]
        E= -df["E"]
    else:
        df.columns = ["conf","E","M"]
        E = df["E"]
    average_energy = np.mean(E)
    energy_dens=average_energy / vol
    return energy_dens

def average_energy_over_Temperature(flag,vol):
    data = extract_txt(flag)
    energy_dens_list = []
    for df in data.values():
        energy_dens = average_energy_density(vol,df,flag)
        energy_dens_list.append(energy_dens)
    temp_list = data.keys()
    return temp_list, energy_dens_list

def plot_average_energy_over_T(flag,vol):
    temp_list,energy_dens_list =average_energy_over_Temperature(flag,vol) 
    plt.Figure()
    plt.plot(temp_list,energy_dens_list,label=f"L={vol}")
    

def Binder_cumulant(vol,df,flag):
    if flag =="Eggwin":
        df.columns = ["conf","M","E"]
    else:
        df.columns = ["conf","E","M"]
    M = df["M"]
    binder_cum = 1 - (np.mean(M**4) / (3 * (np.mean(M**2))**2))
    return binder_cum

def binder_cumulant_over_Temperature(flag,vol):
    data = extract_txt(flag)
    binder_cumulant_list = []
    for df in data.values():
        binder_cumulant = Binder_cumulant(vol,df,flag)
        binder_cumulant_list.append(binder_cumulant)
    temp_list = data.keys()
    return temp_list, binder_cumulant_list

def plot_binder_cumulant_over_T(flag,vol):
    temp_list,binder_cumulant_list =binder_cumulant_over_Temperature(flag,vol) 
    plt.Figure()
    plt.plot(temp_list,binder_cumulant_list,label=f"L={vol}")

volume = {"Eggwin":64, "Beaktrix":256, "Siegfried":1024}
#chicken = ["Eggwin","Beaktrix","Siegfried"]
chicken=["Eggwin"]
#chicken = ["Siegfried"]

for flag in chicken:
    vol = volume[flag]
    plot_abs_av_mgn_over_T(flag,vol)
plt.title("Absolute average magnetisation density over Temperature")
plt.xlabel("T (kB = J = 1)")
plt.ylabel("<|m|>")
plt.legend()
plt.show()

for flag in chicken:
    vol = volume[flag]
    plot_average_energy_over_T(flag,vol)
plt.title("Average energy density over Temperature")
plt.ylabel("<e>")
plt.xlabel("T (kB = J = 1)")
plt.legend()
plt.show()

for flag in chicken:
    vol = volume[flag]
    plot_binder_cumulant_over_T(flag,vol)
plt.title("Binder cumulant over Temperature")
plt.ylabel("B")
plt.xlabel("T (kB = J = 1)")
plt.legend()
plt.show()