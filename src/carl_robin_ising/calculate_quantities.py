#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import bootstrap
from dataset_io import load_yaml  # your helper

# -------------------------------
# Config
# -------------------------------
authors = ['Beaktrix', 'Eggwin', 'Siegfried']

column_mapping = {
    "Beaktrix":  {"C": "column_1", "E": "column_2", "M": "column_3"},
    "Eggwin":    {"C": "column_1", "M": "column_2", "E": "column_3"},
    "Siegfried": {"C": "column_2", "E": "column_3", "M": "column_4"},
}

# Normalizations so M and E become per-site (so we can set V = 1)
norm_M_mapping = {
    "Beaktrix":  1,
    "Eggwin":    8 * 8,
    "Siegfried": 1,
}
norm_E_mapping = {
    "Beaktrix":  -1,     # fix sign if needed
    "Eggwin":    8 * 8,
    "Siegfried": 1,
}

RNG = np.random.default_rng(12345)
N_BOOT = 4000
CONF = 0.95

# -------------------------------
# Helpers
# -------------------------------
def _clean(arr):
    a = np.asarray(arr, dtype=float)
    return a[np.isfinite(a)]

def _ci(x, stat_fn, conf=CONF):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if x.size == 0:
        return (np.nan, np.nan)
    res = bootstrap(
        (x,), stat_fn, confidence_level=conf,
        n_resamples=N_BOOT, method="BCa", random_state=RNG
    )
    return float(res.confidence_interval.low), float(res.confidence_interval.high)

def _mean_ci(x): return _ci(x, np.mean)
def _var_ci(x):  return _ci(x, lambda a: np.var(a, ddof=0))

def susp_from_samples(samples, T, V=1.0):
    """Point estimate for susp using provided samples of M."""
    a = _clean(samples)
    if a.size == 0:
        return np.nan
    return (T / V) * (np.mean(a) - np.var(a, ddof=0))

def susp_ci(x, T, V=1.0):
    """BCa CI for susp by bootstrapping over M directly."""
    return _ci(x, lambda a: (T / V) * (np.mean(a) - np.var(a, ddof=0)))

# -------------------------------
# Load data
# -------------------------------
data = load_yaml("data.yaml")

# -------------------------------
# Main
# -------------------------------
os.makedirs("plots", exist_ok=True)

for author in authors:
    if author not in data or author not in column_mapping:
        continue

    mapping = column_mapping[author]
    temps = data[author].get("temperature", {})
    rows = []

    for t_key, cols in sorted(temps.items(), key=lambda kv: float(kv[0])):
        T = float(t_key)
        V = 1.0  # after per-site normalization

        # pull raw
        E_raw = cols.get(mapping["E"], [])
        M_raw = cols.get(mapping["M"], [])

        # normalize and clean
        E = _clean(E_raw) / norm_E_mapping[author]
        M = _clean(M_raw) / norm_M_mapping[author]

        # point stats
        mean_M = np.mean(M) if M.size else np.nan
        var_M  = np.var(M, ddof=0) if M.size else np.nan
        susp_pt = (T / V) * (var_M) if M.size else np.nan

        # bootstrap CIs
        mean_M_lo, mean_M_hi = _mean_ci(M) if M.size else (np.nan, np.nan)
        var_M_lo,  var_M_hi  = _var_ci(M) if M.size else (np.nan, np.nan)
        susp_lo,    susp_hi  = susp_ci(M, T, V) if M.size else (np.nan, np.nan)

        rows.append(dict(
            T=T,
            susp=susp_pt, susp_lo=susp_lo, susp_hi=susp_hi,
            mean_M=mean_M, mean_M_lo=mean_M_lo, mean_M_hi=mean_M_hi,
            var_M=var_M,   var_M_lo=var_M_lo,   var_M_hi=var_M_hi
        ))

    if not rows:
        continue

    df = pd.DataFrame(rows).sort_values("T")
    out_csv = f"{author}.csv"
    df.to_csv(out_csv, index=False)

    # ---- Plot susp(T) with CI band ----
    plt.figure()
    plt.plot(df["T"], df["susp"], label="susp")
    plt.fill_between(df["T"], df["susp_lo"], df["susp_hi"], alpha=0.3, label="bootstrap CI")
    plt.xlabel("T")
    plt.ylabel("susp")
    plt.title(f"{author}: susceptibility vs T")
    plt.legend()
    plt.tight_layout()
    #out_png = os.path.join("plots", f"{author}_susp.png")
    #plt.savefig(out_png, dpi=150)
    plt.show()
    plt.close()

    #print(f"Wrote {out_csv} and {out_png}")
