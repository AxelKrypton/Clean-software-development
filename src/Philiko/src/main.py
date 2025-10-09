from format_and_average import *
import os
import pathlib as Path
import matplotlib.pyplot as plt
eggwin = {"folder": os.path.join(Path.Path(__file__).parent.parent.parent.parent,"Ising2D/Eggwin/Ising_2D_MCMC_Ns8_Ns8"),
          "grid_size": 8,
          "scaling_m": 64,
          "scaling_E": -256,
		  "col_dict": {"conf":0, "m":1, "E":2}}
beaktrix = {"folder": os.path.join(Path.Path(__file__).parent.parent.parent.parent,"Ising2D/Beaktrix/ising2d_L16"),
          "grid_size": 16,
          "scaling_m": 1,
          "scaling_E": 4,
		  "col_dict": {"conf":0, "m":2, "E":1}}
siegfried = {"folder": os.path.join(Path.Path(__file__).parent.parent.parent.parent,"Ising2D/Siegfried/two_dimensional_ising_model_markov_chain_monte_carlo_Sz32"),
            "grid_size": 32,
            "scaling_m": 1,
            "scaling_E": -4,
            "col_dict": {"conf":1, "m":3, "E":2}}

fig, ax = plt.subplots()
ax1 = ax.twinx()
for chicken in [beaktrix, eggwin, siegfried]:

    df = format_and_average(chicken["folder"], chicken["grid_size"], chicken["scaling_m"], chicken["scaling_E"], chicken["col_dict"])
    ax.plot(df["T"], df["m_mean"], label="m,Eggwin", ls = "None", marker = "o")
    ax1.plot(df["T"], df["E_mean"], label="E,Eggwin", ls = "None", marker = "x")

ax.set_xlabel("T")
ax.set_ylabel("m (o)")
ax1.set_ylabel("E (x)")
plt.show()

