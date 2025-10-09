import pandas as pd
import os

####### TODO: Write in README
#user has to change these values according to input format
#grid_size = 8
#scaling_m = 64
#scaling_E = 256
#input_col [0,1,2]] # id, m, E
###################

def file_parser(file_path, col_dict):
	#assume file has three columns: conf m and E, separated by whitespace
	data = {"m": [], "E": []}
	id = []
	with open(file_path, 'r') as file:
		for line in file:
			if line.startswith('#') or not line.strip():	#skip comment or empty lines
				continue
			parts = line.split()
			if len(parts) >= 2:
				try:
					if parts[col_dict["conf"]] not in id:
						id.append(parts[col_dict["conf"]])
						m_value = float(parts[col_dict["m"]])
						E_value = float(parts[col_dict["E"]])
						data["m"].append(m_value)
						data["E"].append(E_value)
				except ValueError:
					continue
	return pd.DataFrame(data)

def format_data(df, scaling_m, scaling_E):
	if scaling_m == 0 or scaling_E == 0:
		raise ValueError("Scaling factors must be non-zero.")
	df["m"] = df["m"] / scaling_m
	df["E"] = df["E"] / scaling_E
	return df

def average_m_and_E(df):
	return df["m"].mean(), df["E"].mean()

def get_temp_from_filename(file_path):
	base_name = os.path.basename(file_path)
	temp_candidate = []
	counter_dot = 0
	for char in base_name:
		if char.isdigit():
			temp_candidate.append(char)
		elif char == '.' and counter_dot == 0:
			counter_dot += 1
			temp_candidate.append(char)
	temp = ''.join(temp_candidate)
	return float(temp)


def conc_input(file_path, df_out: pd.DataFrame = pd.DataFrame(columns=["T", "m_mean", "E_mean"]), df_input: pd.DataFrame = pd.DataFrame(columns=["m", "E"])):
	T = get_temp_from_filename(file_path)
	m_mean, E_mean = average_m_and_E(df_input)
	df_new = pd.DataFrame({"T": [T], "m_mean": [m_mean], "E_mean": [E_mean]})
	df_out = pd.concat([df_out,df_new], ignore_index=True)
	return df_out

def format_and_average(dir_path, grid_size, scaling_m, scaling_E, dict_cols):
	df_main = pd.DataFrame(columns=["T", "m_mean", "E_mean"])
	for file_name in os.listdir(dir_path):
		file_path = os.path.join(dir_path, file_name)
		df_input = format_data(file_parser(file_path,dict_cols),scaling_m, scaling_E)
		df_main = conc_input(file_path, df_main, df_input)
	return df_main

def __main__(dir_path, grid_size, scaling_m, scaling_E):
	df = format_and_average(dir_path, grid_size, scaling_m, scaling_E)
	print(df.head())
	return