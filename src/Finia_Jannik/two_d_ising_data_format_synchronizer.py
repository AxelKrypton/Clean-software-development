
import pandas as pd
import os
import re

def check_data_folder(folder_path: str):

    """
    Prüft alle .txt-Dateien in einem Ordner auf:
    1. Gleiche Spaltenzahl und -namen.
    2. Korrekte fortlaufende Nummerierung in der ersten Spalte.
    """

    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    if not files:
        print(f"No .txt-files found in {folder_path}.")
        return

    print(f"Check {len(files)} Files in {folder_path} ...\n")

    reference_columns = None
    problems = []

    for filename in files:
        file_path = os.path.join(folder_path, filename)
        df = read_file(file_path)

        # Spaltenvergleich
        if reference_columns is None:
            reference_columns = list(df.columns)
        else:
            if list(df.columns) != reference_columns:
                problems.append((filename, f"Header is not expected: {reference_columns}, gefunden: {list(df.columns)}"))

        # Erste Spalte prüfen (Nummerierung)
        first_col = df.iloc[:, 0]
        if not pd.api.types.is_numeric_dtype(first_col):
            problems.append((filename, "First column is not numerical"))
            continue
        
        # Prüfen auf Duplikate oder Lücken
        diffs = first_col.diff().dropna()
        
        if not all(diffs == 1):
            missing = set(range(int(first_col.min()), int(first_col.max()) + 1)) - set(first_col)
            has_duplicates = df.duplicated().any()
            messages = []
            if missing:
                messages.append(f"Jumps: {sorted(list(missing))[:10]}{' ...' if len(missing) > 10 else ''}")
            if has_duplicates:
                df = df.drop_duplicates()
                messages.append(f"There are duplicates")
            if messages:
                problems.append((filename, "; ".join(messages)))
    
    # Zusammenfassung
    if not problems:
        print("✅ Alle Dateien sind im gleichen Format!")
    else:
        print("⚠️ Probleme gefunden:\n")
        #for fname, issue in problems:
        #    print(f" - {fname}: {issue}")

    return problems

def read_file(file_path):
    try:
        with open(file_path, 'r') as f:
            first_line = f.readline().strip()
        has_header = first_line.startswith('#')
        if has_header:
            header_line = first_line.lstrip('#').strip()
            columns = header_line.split()
            df = pd.read_csv(file_path, comment = '#', sep='\s+', names = columns, skiprows = 1, engine = 'python')
        else:
            
            if 'Beaktrix' in file_path:
                columns = ['conf', 'E', 'M']
                df = pd.read_csv(file_path, comment = '#', sep='\s+', names = columns, engine='python')
         
            if 'Siegfried' in file_path:
                columns = ['temp', 'conf', 'E', 'M']
                df = pd.read_csv(file_path, comment = '#', sep='\s+', names = columns, engine='python')
         
    except Exception as e:
        print((file_path, f"Error reading file: {e}"))
    return df


def synchronize_data(folder_path: str):

    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    Data = {}

    for filename in files:
        file_path = os.path.join(folder_path, filename)
        df = read_file(file_path)

        if 'Siegfried' in file_path:
            df = df.drop(columns = ['temp', 'conf'])
            #temp = filename[1:5].rstrip('.')
            # Todo: read temp from file column, not name!!
            
        elif 'Beaktrix' in file_path:
            df = df.drop(columns = ['conf'])

        elif 'Eggwin' in file_path:
            df = df.drop(columns = ['conf'])
            #temp = filename[4:8].rstrip('.')

        temp = re.search(r"(-?\d+(?:\.\d+)?)",filename).group(1)

        Data[temp] = df

    return Data

    