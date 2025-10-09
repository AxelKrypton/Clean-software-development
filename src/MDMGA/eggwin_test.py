import sys
import os

import pytest
import numpy

from conversion import Eggwin


def test_existing_ensemble_exists():
    lattice_size = 8
    eggwin = Eggwin(lattice_size)
    assert os.path.isdir(eggwin.ensemble_data_path)


def test_constructing_with_not_existing_ensemble_raises_error():
    lattice_size = 15
    with pytest.raises(ValueError):
        eggwin = Eggwin(lattice_size)


def test_find_correct_number_of_temperatures():
    lattice_size = 8
    number_of_temperatures = 34
    eggwin = Eggwin(lattice_size)
    assert number_of_temperatures == len(eggwin.temperatures)


def test_extract_temperature_from_existing_file():
    lattice_size = 8
    eggwin = Eggwin(lattice_size)
    temperatures = [0.5, 0.8, 1.1]
    for temperature in temperatures:
        assert temperature == Eggwin.get_temperature_from_file_name(eggwin.ensemble_data_path + r"/temp"f"{temperature}"r".txt")


def test_certain_temperatures_exist():
    lattice_size = 8
    temperatures = [0.5, 0.8, 1.1]
    eggwin = Eggwin(lattice_size)
    for temperature in temperatures:
        assert temperature in eggwin.temperatures


def test_all_files_can_be_loaded():
    lattice_size = 8
    eggwin = Eggwin(lattice_size)
    for temperature in eggwin.temperatures:
        assert temperature in eggwin.data.keys()


def test_all_data_has_3_columns():
    lattice_size = 8
    eggwin = Eggwin(lattice_size)
    for temperature in eggwin.temperatures:
        assert eggwin.data[temperature].shape[1] == 3


def test_e_and_m_are_switched_and_normalized():
    lattice_size = 8
    eggwin = Eggwin(lattice_size)
    temperatures = [0.5, 0.8, 1.1]
    for temperature in temperatures:
        file_name = eggwin.get_file_name_input(temperature)
        data = numpy.loadtxt(file_name)
        assert numpy.all(data[:, 1] / (lattice_size * lattice_size) == eggwin.data[temperature][:, 2])
        assert numpy.all(data[:, 2] / (lattice_size * lattice_size * 4.0) == eggwin.data[temperature][:, 1])


def test_file_name_output():
    lattice_size = 8
    output_paths = ["", "asdf/"]
    for output_path in output_paths:
        eggwin = Eggwin(lattice_size, output_path)
        for temperature in eggwin.temperatures:
            file_name_output = output_path + f"Ising2D_L{lattice_size}_T{temperature:.2f}.csv"
            assert eggwin.get_file_name_output(temperature) == file_name_output


def test_produce_output():
    lattice_size = 8
    output_path = os.path.dirname(os.path.abspath(__file__)) + f"/test_output/"
    eggwin = Eggwin(lattice_size, output_path)
    eggwin.save_data()
    for temperature in eggwin.temperatures:
        file_name_output = eggwin.get_file_name_output(temperature)
        assert os.path.isfile(file_name_output)
