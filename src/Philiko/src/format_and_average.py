import pandas as pd

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

def average_data(df):
	pass

def parse_file_name(file_path):
	pass

def conc_input(file_path):
	parse_file_name(file_path)
	average_data(file_parser(file_path))

def format_and_average(file_path, grid_size, scaling_m, scaling_E):
	df_input = file_parser(file_path)
	df_main = conc_input(file_path)
	df_cleaned = format_data(df, scaling_m, scaling_E)
	df_averaged = average_data(df_cleaned)
	return df_averaged