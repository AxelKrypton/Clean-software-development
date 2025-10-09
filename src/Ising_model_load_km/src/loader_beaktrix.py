import os
import sys
import numpy as np
import warnings

data_type = tuple[int, list[float], list[np.ndarray], list[np.ndarray]]
def loader_beaktrix() -> data_type:
    beaktrix_dir = os.path.join(
        os.path.dirname(__file__), "../../../Ising2D/Beaktrix/ising2d_L16/"
    )
    L = 16

    temperatures: list = []
    energy_densities: list[np.array] = []
    magnetizations: list[np.array] = []

    for file in sorted(os.listdir(beaktrix_dir)):

        file_path = os.path.join(beaktrix_dir, file)
        if os.path.isfile(file_path):

            file_name = os.path.basename(file_path)
            temperature = float(file_name[1:-4])
            
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    data = np.genfromtxt(file_path, skip_header=0, filling_values=0.0, dtype=float, invalid_raise=False, usemask=False)
            except ValueError as e:
                print(f"Error reading {file_path}: {e}", file=sys.stderr)
                continue

            energy_density = []
            magnetization = []

            for row in data:
                energy_density.append(row[1])
                magnetization.append(row[2])

            temperatures.append(temperature)
            energy_densities.append(energy_density)
            magnetizations.append(magnetization)

    # TODO check for normalization
    return L, temperatures, energy_densities, magnetizations

loader_beaktrix()