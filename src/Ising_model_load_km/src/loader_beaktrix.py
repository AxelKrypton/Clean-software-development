import os
import sys

import numpy

beaktrix_dir = sys.path.insert(
    1,
    os.path.join(
        os.path.dirname(__file__), "../../../Ising2D/Beaktrix/ising2d_L16/"
    ),
)

def loader_beaktrix(path: str) -> None:
    pass
