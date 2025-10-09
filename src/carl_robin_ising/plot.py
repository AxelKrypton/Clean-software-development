#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 17:09:18 2025

@author: carl
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
authors=["Eggwin","Beaktrix","Siegfried"]
author_to_lattice = {"Beaktrix": "L=16",
                     "Eggwin": "L=8",
                     "Siegfried": "L=4"
                     }
# Load the data
for author in authors:
    data = pd.read_csv(author+".csv")

    # Plot the main curve
    plt.plot(data["T"], data["susp"], label=author_to_lattice[author])

    # Fill between lower and upper error bands
    #plt.fill_between(data["T"], data["susp_lo"], data["susp_hi"], alpha=0.3)


# Optional labels and legend
plt.xlabel("T")
plt.ylabel(r"$\chi_{\mathrm{absM}}$")
plt.legend()
plt.tight_layout()
plt.show()
