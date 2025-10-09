from format_and_average import *
import os
import pathlib as Path
import matplotlib.pyplot as plt
eggwin = {"folder": os.path.join(Path.Path(__file__).parent.parent.parent.parent,"Ising2D/Eggwin/Ising_2D_MCMC_Ns8_Ns8"),
          "grid_size": 8,
          "scaling_m": 64,
          "scaling_E": 256}
beaktrix = {"folder": os.path.join(Path.Path(__file__).parent.parent.parent.parent,"Ising2D/Beaktrix/ising2d_L16"),
          "grid_size": 16,
          "scaling_m": 1,
          "scaling_E": 4}


df_eggwin = format_and_average(eggwin["folder"], eggwin["grid_size"], eggwin["scaling_m"], eggwin["scaling_E"])
fig, ax = plt.subplots()
ax1 = ax.twinx()
ax.plot(df_eggwin["T"], df_eggwin["m_mean"], label="m,Eggwin", ls = "None", marker = "o")
ax1.plot(df_eggwin["T"], df_eggwin["E_mean"], label="E,Eggwin", ls = "None", marker = "x", color = "orange")
ax.set_xlabel("T")
ax.set_ylabel("m (o)")
ax1.set_ylabel("E (x)")
plt.show()

