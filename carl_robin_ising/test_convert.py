# tests/test_yaml_consistency.py
import numpy as np
import pytest
from dataset_io import load_yaml, build_from_sources

# Adjust paths to your repo layout as needed
YAML_PATH = "data.yaml"
ROOT_GLOB = "../Ising2D/*"
IGNORE_AUTHORS = {"MDMGA"}  # you excluded it when creating YAML

ATOL = 1e-12
RTOL = 1e-12
COL_KEYS = ["column_1", "column_2", "column_3", "column_4"]

def _allclose_lists(a, b, rtol=RTOL, atol=ATOL):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != b.shape:
        return False
    return np.allclose(a, b, rtol=rtol, atol=atol, equal_nan=True)

def test_yaml_matches_sources():
    yaml_data = load_yaml(YAML_PATH)
    src_data  = build_from_sources(ROOT_GLOB, ignore_authors=IGNORE_AUTHORS)

    # Authors must match (minus ignored)
    assert set(yaml_data.keys()) == set(src_data.keys()), \
        f"Authors differ: yaml={set(yaml_data.keys())}, src={set(src_data.keys())}"

    for author in yaml_data.keys():
        y_t = yaml_data[author].get("temperature", {})
        s_t = src_data[author].get("temperature", {})

        # Temperature keys must match (string keys like '0.5')
        assert set(y_t.keys()) == set(s_t.keys()), \
            f"[{author}] Temps differ: yaml={set(y_t.keys())}, src={set(s_t.keys())}"

        for temp_key in y_t.keys():
            y_cols = y_t[temp_key]
            s_cols = s_t[temp_key]

            # Ensure same column keys
            assert set(y_cols.keys()) == set(COL_KEYS)
            assert set(s_cols.keys()) == set(COL_KEYS)

            # Compare each column numerically with tolerance
            for ck in COL_KEYS:
                ya = y_cols[ck]
                sa = s_cols[ck]
                assert _allclose_lists(ya, sa), \
                    f"[{author} @ T={temp_key}] Column {ck} mismatch.\nYAML: {ya}\nSRC:  {sa}"
