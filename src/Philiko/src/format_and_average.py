import pandas as pd

df_main = pd.DataFrame()

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
	return format_data(pd.DataFrame(data))

def format_data(df):
	pass

def average_data(df):
	pass

def parse_file_name(file_path):
	pass

def conc_input(file_path):
	parse_file_name(file_path)
	average_data(file_parser(file_path))

def format_and_average(file_path):
	df_input = file_parser(file_path)
	df_main = conc_input(file_path)
	df_cleaned = format_data(df)
	df_averaged = average_data(df_cleaned)
	return df_averaged