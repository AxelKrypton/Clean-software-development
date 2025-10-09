import os
import sys

import numpy

siegfried_dir = sys.path.insert(
    1,
    os.path.join(
        os.path.dirname(__file__),
        "../../../Ising2D/Siegfried/two_dimensional_ising_model_markov_chain_monte_carlo_Sz32/",
    ),
)

# Temperature, measurement index, energy density, magnetization
def loader_siegfried(path: str) -> None:
    pass

    # return L, np.ndarray (temp), np.ndarray 2D (energy density), np.ndarray 2D (magnetization)
