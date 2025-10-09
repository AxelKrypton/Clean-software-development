import two_d_ising_data_format_synchronizer as formatter

eggwin = 'Eggwin/Ising_2D_MCMC_Ns8_Ns8'
beaktrix = 'Beaktrix/ising2d_L16'
siegfried = 'Siegfried/two_dimensional_ising_model_markov_chain_monte_carlo_Sz32'

folder_path_siegfried = '../../Ising2D/'+ siegfried
folder_path_beaktrix = '../../Ising2D/'+ beaktrix
folder_path_eggwin = '../../Ising2D/'+ eggwin

#folder_path = 'tests/test_data/Eggwin/corrupted_data_conf/'

check = formatter.check_data_folder(folder_path_siegfried)
#print(check)

# Read data of all files for each chicken as Dictionary with temperature as keys
# and dataframes as values including E and M as columns
Data_Siegfried = formatter.synchronize_data(folder_path_siegfried)
Data_Beaktrix = formatter.synchronize_data(folder_path_beaktrix)
Data_Eggwin = formatter.synchronize_data(folder_path_eggwin)

print(Data_Siegfried['2.2']['E'])
print(Data_Beaktrix.keys())
print(Data_Eggwin.keys())

