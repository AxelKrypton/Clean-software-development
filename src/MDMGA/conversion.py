import os

import numpy


class Eggwin:
    ensemble_data_path_prefix = "../Eggwin/"

    def get_ensemble_data_path(lattice_size: int) -> str:
        return Eggwin.ensemble_data_path_prefix + f"Ising_2D_MCMC_Ns{lattice_size}_Ns{lattice_size}"
    
    def get_temperature_from_file_name(file_name: str) -> float:
        file_name = file_name.split(r"/")[-1]
        file_name = file_name[len("temp"):]
        file_name = file_name[:- len(".txt")]
        return float(file_name)
    
    def get_temperatures_for_ensemble(ensemble_data_path: str) -> list[float]:
        files = os.scandir(ensemble_data_path)
        temperatures = []
        for file in files:
            if file.is_file():
                temperatures.append(Eggwin.get_temperature_from_file_name(os.path.basename(file)))
        return temperatures

    def __init__(self, lattice_size: int, output_path: str | None = None):
        self.lattice_size = lattice_size
        self.output_path = output_path
        if output_path is None:
            self.output_path = "./"
        self.ensemble_data_path = Eggwin.get_ensemble_data_path(lattice_size)
        if not os.path.isdir(self.ensemble_data_path):
            raise ValueError(f"Data path does not exist for lattice size {lattice_size}")
        self.temperatures = Eggwin.get_temperatures_for_ensemble(self.ensemble_data_path)
        for temperature in self.temperatures:
            self.load_data(temperature)

    def get_file_name_input(self, temperature: float) -> str:
        return self.ensemble_data_path + f"/temp{temperature:.1f}.txt"
    
    def get_file_name_output(self, temperature: float) -> str:
        return self.output_path + f"Ising2D_L{self.lattice_size}_T{temperature:.2f}.csv"
    
    def load_data(self, temperature: float):
        if not hasattr(self, "data"):
            self.data = {}
        data = numpy.loadtxt(self.get_file_name_input(temperature))
        self.data[temperature] = numpy.empty(data.shape)
        self.data[temperature][:, 0] = data[:, 0]
        self.data[temperature][:, 1] = data[:, 2] / (self.lattice_size * self.lattice_size * 4.0)
        self.data[temperature][:, 2] = data[:, 1] / (self.lattice_size * self.lattice_size)

    def save_data(self):
        for temperature, data in self.data.items():
            numpy.savetxt(self.get_file_name_output(temperature), data, fmt="         %04d  %+.15e  %+.15e", header="measurement                       E                       M")


def main():
    pass


if __name__ == "__main__":
    main()

