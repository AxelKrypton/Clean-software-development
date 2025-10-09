import pandas as pd
from pathlib import Path
import os
import numpy as np
import warnings
from tqdm import tqdm
import re

warnings.filterwarnings("ignore", category=SyntaxWarning)

base_path = os.path.join(os.getcwd())
base_path= base_path + "/MDMGA/"
print(f"base path check if in Ising2D: {base_path}")

data_paths = {
    "Eggwin": "Eggwin/",
    "Beatrix": "Beatrix/",
    "Siegfried": "Siegfried/"
}

data_path_full_list = []
files_list = []
for name in data_paths:
    data_path_full = base_path + data_paths[name]
    files = [f for f in os.listdir(data_path_full) if os.path.isfile(os.path.join(data_path_full, f))]
    files_list.append(files)

    data_path_full_list.append(data_path_full)
    print(data_path_full)

print(data_path_full_list)

E_eggwin_avg, M_eggwin_avg, E_eggwin_std, M_eggwin_std, T_eggwin_list = [], [], [], [], []
for file in tqdm(files_list[0], desc="Processing eggwin", unit="folder"):
    file_path = os.path.join(data_path_full_list[0], file)
    df = pd.read_csv(file_path, sep=r'\s+', comment="#", names=["conf", "E", "M"])

    E_vals = df["E"]
    M_vals = df["M"]

    file_name = os.path.splitext(os.path.basename(file_path))[0]  
    match = re.search(r"[-+]?\d*\.?\d+", file_name)  # Matches integers or decimals
    if match:
        T_val = float(match.group())
        T_eggwin_list.append(T_val)
        E_eggwin_avg.append(E_vals.mean())
        M_eggwin_avg.append(M_vals.mean())
        E_eggwin_std.append(E_vals.std())
        M_eggwin_std.append(M_vals.std())

E_beatrix_avg, M_beatrix_avg, E_beatrix_std, M_beatrix_std, T_beatrix_list = [], [], [], [], []
for file in tqdm(files_list[1], desc="Processing beatrix", unit="folder"):
    file_path = os.path.join(data_path_full_list[1], file)
    df = pd.read_csv(file_path, sep=r'\s+', comment="#", names=["conf", "E", "M"])

    E_vals, M_vals = df["E"], df["M"]
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    match = re.search(r"[-+]?\d*\.?\d+", file_name)
    if match:
        T_val = float(match.group())
        T_beatrix_list.append(T_val)
        E_beatrix_avg.append(E_vals.mean())
        M_beatrix_avg.append(M_vals.mean())
        E_beatrix_std.append(E_vals.std())
        M_beatrix_std.append(M_vals.std())

E_siegfried_avg, M_siegfried_avg, E_siegfried_std, M_siegfried_std, T_siegfried_list = [], [], [], [], []
for file in tqdm(files_list[2], desc="Processing siegfried", unit="folder"):
    file_path = os.path.join(data_path_full_list[2], file)
    df = pd.read_csv(file_path, sep=r'\s+', comment="#", names=["conf", "E", "M"])

    E_vals, M_vals = df["E"], df["M"]
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    match = re.search(r"[-+]?\d*\.?\d+", file_name)
    if match:
        T_val = float(match.group())
        T_siegfried_list.append(T_val)
        E_siegfried_avg.append(E_vals.mean())
        M_siegfried_avg.append(M_vals.mean())
        E_siegfried_std.append(E_vals.std())
        M_siegfried_std.append(M_vals.std())
#check the arrays of the 3 chickens
        
vars_to_check = [
    "E_eggwin_avg", "M_eggwin_avg", "T_eggwin_list",
    "E_beatrix_avg", "M_beatrix_avg", "T_beatrix_list",
    "E_siegfried_avg", "M_siegfried_avg", "T_siegfried_list"
]

[print(v, np.shape(globals()[v])) for v in vars_to_check]

# plotting yay
        
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 3, figsize=(12, 8))
colors = ["#8B5FBF", "#0072B2", "#009E73"]

# 1st row: M vs T with errorbars
axes[0, 0].errorbar(T_eggwin_list, M_eggwin_avg, yerr=M_eggwin_std, fmt="o", color=colors[0], label="Eggwin")
axes[0, 1].errorbar(T_beatrix_list, M_beatrix_avg, yerr=M_beatrix_std, fmt="o", color=colors[1], label="Beatrix")
axes[0, 2].errorbar(T_siegfried_list, M_siegfried_avg, yerr=M_siegfried_std, fmt="o", color=colors[2], label="Siegfried")

# 2nd row: E vs T with errorbars
axes[1, 0].errorbar(T_eggwin_list, E_eggwin_avg, yerr=E_eggwin_std, fmt="o", color=colors[0], label="Eggwin")
axes[1, 1].errorbar(T_beatrix_list, E_beatrix_avg, yerr=E_beatrix_std, fmt="o", color=colors[1], label="Beatrix")
axes[1, 2].errorbar(T_siegfried_list, E_siegfried_avg, yerr=E_siegfried_std, fmt="o", color=colors[2], label="Siegfried")

for i in range(3):
    axes[0, i].set_xlabel("T")
    axes[0, i].set_ylabel("M")
    axes[0, i].legend()
    axes[1, i].set_xlabel("T")
    axes[1, i].set_ylabel("E")
    axes[1, i].legend()

plt.tight_layout()
plt.show()