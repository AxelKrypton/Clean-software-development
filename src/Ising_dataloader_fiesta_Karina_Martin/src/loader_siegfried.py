import os

import numpy as np

data_type = tuple[int, list[float], list[np.ndarray], list[np.ndarray]]


def loader_siegfried() -> data_type:
    """Load data from siegfried files.

    Special which have to be covered for loading this files:
    - Datapoints per file is not constant

    Returns:
        lattice_size (int): The lattice size.
        temperature (list[float]): A 1D list of temperatures.
        energy_density (list[np.ndarray]):
          List of length [n_files] containing numpy arrays, each of size [n_datapoints],
          containing the energy densities.
        magnetization (list[np.ndarray]):
          List of length [n_files] containing numpy arrays, each of size [n_datapoints],
          containing the magnetizations.

    """
    siegfried_dir: str = os.path.join(
        os.path.dirname(__file__),
        "../../../Ising2D/Siegfried/two_dimensional_ising_model_markov_chain_monte_carlo_Sz32",
    )
    file_list: list[str] = [f for f in os.listdir(siegfried_dir) if f.endswith(".txt")]
    file_list.sort()

    temperature: list = []
    energy_density: list[np.ndarray] = []
    magnetization: list[np.ndarray] = []

    for file_name in file_list:
        file_temp: float = float(file_name[1:-4])
        temperature.append(file_temp)
        data: np.ndarray = np.genfromtxt(
            os.path.join(siegfried_dir, file_name), delimiter="  ", dtype=np.float32
        )
        energy_density.append(data[:, 2])
        magnetization.append(data[:, 3])

    lattice_size: int = 32
    return lattice_size, temperature, energy_density, magnetization


if __name__ == "__main__":
    loader_siegfried()
