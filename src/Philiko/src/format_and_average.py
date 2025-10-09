import pandas as pd
import os

df_main = pd.DataFrame()

####### TODO: Write in README
#user has to change these values according to input format
#grid_size = 8
#scaling_m = 64
#scaling_E = 256

def file_parser(file_path):
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
					if parts[0] not in id:
						id.append(parts[0])
						m_value = float(parts[1])
						E_value = float(parts[2])
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


def conc_input(file_path):
	T = get_temp_from_filename(file_path)
	m_mean, E_mean = average_m_and_E(file_parser(file_path))

def format_and_average(file_path, grid_size, scaling_m, scaling_E):
	df_input = file_parser(file_path)
	df_main = conc_input(file_path)
	df_cleaned = format_data(df, scaling_m, scaling_E)
	df_averaged = average_data(df_cleaned)
	return df_averaged