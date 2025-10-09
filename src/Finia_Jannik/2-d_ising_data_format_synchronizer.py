
import pandas as pd
import os

def check_data_folder(folder_path: str):
    """
    Prüft alle .txt-Dateien in einem Ordner auf:
    1. Gleiche Spaltenzahl und -namen.
    2. Korrekte fortlaufende Nummerierung in der ersten Spalte.
    """
    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    if not files:
        print(f"Keine .txt-Dateien in {folder_path} gefunden.")
        return

    print(f"Überprüfe {len(files)} Dateien in {folder_path} ...\n")

    # Basisformat (Header) speichern
    reference_columns = None
    problems = []

    for filename in files:
        file_path = os.path.join(folder_path, filename)
        try:
            df = pd.read_csv(file_path, sep=None, engine='python')  # automatisches Separator-Erkennen
        except Exception as e:
            problems.append((filename, f"Fehler beim Einlesen: {e}"))
            continue

        # Spaltenvergleich
        if reference_columns is None:
            reference_columns = list(df.columns)
        else:
            if list(df.columns) != reference_columns:
                problems.append((filename, f"Header stimmt nicht überein. Erwartet: {reference_columns}, gefunden: {list(df.columns)}"))

        # Erste Spalte prüfen (Nummerierung)
        first_col = df.iloc[:, 0]
        if not pd.api.types.is_numeric_dtype(first_col):
            problems.append((filename, "Erste Spalte ist nicht numerisch."))
            continue

        # Prüfen auf Duplikate oder Lücken
        diffs = first_col.diff().dropna()
        if not all(diffs == 1):
            missing = set(range(int(first_col.min()), int(first_col.max()) + 1)) - set(first_col)
            duplicates = first_col[first_col.duplicated()].tolist()
            msg = []
            if missing:
                msg.append(f"Lücken: {sorted(list(missing))[:10]}{' ...' if len(missing) > 10 else ''}")
            if duplicates:
                msg.append(f"Duplikate: {duplicates}")
            if msg:
                problems.append((filename, "; ".join(msg)))

    # Zusammenfassung
    if not problems:
        print("✅ Alle Dateien sind im gleichen Format und korrekt nummeriert.")
    else:
        print("⚠️ Probleme gefunden:\n")
        for fname, issue in problems:
            print(f" - {fname}: {issue}")
