import os
import sys
import warnings

import numpy as np

data_type = tuple[int, list[float], list[np.ndarray], list[np.ndarray]]


def loader_beaktrix() -> data_type:
    """Load Beaktrix data for 2D Ising model simulations.

    Returns:
        data_type:
        - beaktrix_l = size of the lattice
        - temperatures = list of temperatures from different measurements
        - energy_densities: list of np.array each containing
           energy density measurements at the same temperature
        - magnetizations: list of np.array each containing
           magnetization measurements at the same temperature

    Note:
        - the Beaktrix data files are expected to be located in the directory
          beaktrix_dir
        - each file is expected to be named in the format "T{temperature}.txt"
          where {temperature} is a float representing the temperature of the
          measurements
        - each file is expected to contain three columns:
          1. Measurement index (not used)
          2. Energy density measurements
          3. Magnetization measurements
        - files that cannot be read will be skipped with a warning
        - single lines with less than 3 columns will be filltered and removed.
          The warning for that action is suppressed.
        - the function returns the data sorted by temperature

    """
    beaktrix_dir = os.path.join(
        os.path.dirname(__file__), "../../../Ising2D/Beaktrix/ising2d_L16/"
    )
    beaktrix_l = 16

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
                    data: np.ndarray = np.genfromtxt(
                        file_path,
                        skip_header=0,
                        filling_values=0.0,
                        dtype=float,
                        invalid_raise=False,
                        usemask=False,
                    )
            except ValueError as e:
                print(f"Error reading {file_path}: {e}", file=sys.stderr)
                continue

            temperatures.append(temperature)
            energy_densities.append(data[:, 1])
            magnetizations.append(data[:, 2])

    # TODO(karina): check for normalization
    return beaktrix_l, temperatures, energy_densities, magnetizations


if __name__ == "__main__":
    loader_beaktrix()
