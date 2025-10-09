import pandas as pd
from pathlib import Path
import os
import numpy as np
import warnings
from tqdm import tqdm


warnings.filterwarnings("ignore", category=SyntaxWarning)

#base_path = "/Users/vilijadejonge/Downloads/Clean-software-development/Ising2D/" 
base_path = os.path.join(os.getcwd())
base_path= base_path + "/src/"
print(f"base path check if in Ising2D: {base_path}")


data_paths = {
    "Eggwin": "Eggwin/Ising_2D_MCMC_Ns8_Ns8",
    "Beatrix": "Beaktrix/ising2d_L16",
    "Siegfried": "Siegfried/two_dimensional_ising_model_markov_chain_monte_carlo_Sz32"
}

output_base = base_path + "MDMGA/"

data_dir_list = []
output_dir_list = []
folder_path_list = []
files_list = [] 
for name, rel_path in data_paths.items():
    data_dir = base_path + rel_path
    data_dir_list.append(data_dir)
    output_dir = output_base + name
    output_dir_list.append(output_dir)

    os.makedirs(output_dir, exist_ok=True)
    #print(output_dir)

    if os.path.exists(data_dir):
        folder_path = data_dir
        folder_path_list.append(folder_path)
        print(f"found folder {folder_path}")
    else:
        print(f"didn't find folder {folder_path}")
    

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    files_list.append(files)
    num_files = len(files)


#Eggwin restructuing data and fixing errors
for file in tqdm(files_list[0], desc="Processing eggwin", unit="folder"):
    L = 8
    V = L**2
    file_path = os.path.join(folder_path_list[0], file)
    df = pd.read_csv(file_path, sep=r'\s+', comment="#", names=["conf", "E", "M"])

    E_original = df["E"]
    M_original = df["M"]
    E_correct = M_original
    M_correct = E_original
    E_correct_norm = -E_correct / (4 * V)
    M_correct_norm = M_correct / V

    file_name = os.path.splitext(os.path.basename(file_path))[0]  

    df_out = pd.DataFrame({
            "conf": df["conf"],
            "E": E_correct_norm,
            "M": M_correct_norm
        })
 
    out_file = os.path.join(output_dir_list[0], f"{file_name}_formatted.csv")
    with open(out_file, "w") as f:
        f.write("# conf    E           M\n")
        for _, row in df_out.iterrows():
            f.write(f"{row['conf']:8.1f} {row['E']:10.6f} {row['M']:10.6f}\n")


    #print(f"File saved to: {out_file}")
nearest_neighbors = 4
#Beatrix restructuing data and fixing errors
for file in tqdm(files_list[1], desc="Processing beatrix", unit="folder"):
    file_path = os.path.join(folder_path_list[1], file)
    df = pd.read_csv(file_path, sep=r'\s+', names=["conf", "E", "M"])#.to_numpy()

    E_correct = df["E"]
    M_correct =  df["M"]
    E_correct_norm = E_correct / nearest_neighbors
    M_correct_norm = M_correct

    file_name = os.path.splitext(os.path.basename(file_path))[0]

    df_out = pd.DataFrame({
            "conf": df["conf"],
            "E": E_correct_norm,
            "M": M_correct_norm
        })
 
    out_file = os.path.join(output_dir_list[1], f"{file_name}_formatted.csv")
    with open(out_file, "w") as f:
        f.write("# conf    E           M\n")
        for _, row in df_out.iterrows():
            f.write(f"{row['conf']:8.1f} {row['E']:10.6f} {row['M']:10.6f}\n")


    #print(f"File saved to: {out_file}")

#Siegfried restructuing data and fixing errors
for file in tqdm(files_list[2], desc="Processing siegfried", unit="folder"):  
    file_path = os.path.join(folder_path_list[2], file)
    df = pd.read_csv(file_path, sep=r'\s+', usecols=[1, 2, 3], names=["conf", "E", "M"])#.to_numpy()

    E_correct = df["E"]
    M_correct =  df["M"]
    E_correct_norm = -E_correct /nearest_neighbors 
    M_correct_norm = M_correct 

    file_name = os.path.splitext(os.path.basename(file_path))[0]  

    df_out = pd.DataFrame({
            "conf": df["conf"],
            "E": E_correct_norm,
            "M": M_correct_norm
        })
 
    out_file = os.path.join(output_dir_list[2], f"{file_name}_formatted.csv")
    with open(out_file, "w") as f:
        f.write("# conf    E           M\n")
        for _, row in df_out.iterrows():
            f.write(f"{row['conf']:8.1f} {row['E']:10.6f} {row['M']:10.6f}\n")


    #print(f"File saved to: {out_file}")
print("All done!")
