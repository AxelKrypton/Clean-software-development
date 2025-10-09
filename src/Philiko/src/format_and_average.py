import pandas as pd

def input_parser(file_path):
	#assume file has three columns: conf m and E, separated by whitespace
	data = {"m": [], "E": []}
	with open(file_path, 'r') as file:
		for line in file:
			if line.startswith('#') or not line.strip():	#skip comment or empty lines
				continue
			parts = line.split()
			if len(parts) >= 2:
				try:
					m_value = float(parts[1])
					E_value = float(parts[2])
					data["m"].append(m_value)
					data["E"].append(E_value)
				except ValueError:
					continue
	return pd.DataFrame(data)