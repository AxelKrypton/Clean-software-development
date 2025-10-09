import os
import sys

import numpy

eggwin_dir = sys.path.insert(
    1,
    os.path.join(
        os.path.dirname(__file__), "../../../Ising2D/Eggwin/Ising_2D_MCMC_Ns8_Ns8/"
    ),
)

def loader_eggwin(path: str) -> None:
    pass
