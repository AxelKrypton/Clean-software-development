# dataset_io.py
import os
import glob
import re
import yaml
import pandas as pd

def _temperature_from_filename(name: str) -> str:
    """Extract first number from filename and return it as a string key (e.g. '0.5')."""
    m = re.search(r"[-+]?(?:\d*\.\d+|\d+)", name)
    if not m:
        raise ValueError(f"No temperature found in filename: {name}")
    return str(float(m.group(0)))  # normalize like '0.5', '2.0', etc.

def _read_txt_as_columns(path: str) -> dict:
    """
    Read whitespace- (or comma-) separated numeric TXT into up to 4 flat lists.
    Mirrors the YAML-building logic.
    """
    df = pd.read_csv(
        path,
        sep=r"\s+",
        comment="#",
        header=None,
        engine="python",
    )
    df = df.dropna(axis=1, how="all")
    ncols = min(4, df.shape[1])

    def col(i):
        return df.iloc[:, i].astype(float).tolist() if ncols >= i + 1 else []

    return {
        "column_1": col(0),
        "column_2": col(1),
        "column_3": col(2),
        "column_4": col(3),
    }

def load_yaml(yaml_path: str) -> dict:
    """Load YAML and normalize temperature keys to strings for stable comparison."""
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f) or {}

    # Normalize temp keys to strings
    for author, a_data in list(data.items()):
        temps = a_data.get("temperature", {})
        if not isinstance(temps, dict):
            continue
        if any(not isinstance(k, str) for k in temps.keys()):
            # re-map with str(float(k))
            new_temps = {}
            for k, v in temps.items():
                key_str = str(float(k)) if isinstance(k, (int, float)) else str(k)
                new_temps[key_str] = v
            a_data["temperature"] = new_temps
    return data

def build_from_sources(root_glob: str = "../Ising2D/*", ignore_authors=None) -> dict:
    """
    Recreate the structure directly from the TXT files so it can be compared to YAML.
    ignore_authors: optional set/list of author folder names to skip (e.g., {'MDMGA'})
    """
    ignore = set(ignore_authors or [])
    result = {}

    folders = glob.glob(root_glob)
    for folder in folders:
        author = os.path.basename(folder)
        if author in ignore:
            continue

        temps_dict = {}
        text_files = glob.glob(os.path.join(folder, "*", "*.txt"))
        for f in sorted(text_files):
            temp_key = _temperature_from_filename(os.path.basename(f))  # string key
            temps_dict[temp_key] = _read_txt_as_columns(f)

        result[author] = {"temperature": temps_dict}
    return result
