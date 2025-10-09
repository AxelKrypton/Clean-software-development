import os
import sys

import numpy as np
import pytest

sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
from src.loader_beaktrix import loader_beaktrix

data_type = tuple[int, list[float], list[np.ndarray], list[np.ndarray]]


@pytest.fixture(scope="module")
def get_data_loader_beaktrix() -> data_type:
    return loader_beaktrix()


def test_l(get_data_loader_beaktrix: data_type) -> None:
    output_l, _, _, _ = get_data_loader_beaktrix
    expected_l = 16
    assert output_l == expected_l


def test_length_temperatures(get_data_loader_beaktrix: data_type) -> None:
    _, temperatures, _, _ = get_data_loader_beaktrix
    expected_number_of_files = 28
    assert len(temperatures) == expected_number_of_files


def test_length_energy_densities(get_data_loader_beaktrix: data_type) -> None:
    _, _, energy_densities, _ = get_data_loader_beaktrix
    expected_number_of_files = 28
    assert len(energy_densities) == expected_number_of_files


def test_length_magnetizations(get_data_loader_beaktrix: data_type) -> None:
    _, _, _, magnetizations = get_data_loader_beaktrix
    expected_number_of_files = 28
    assert len(magnetizations) == expected_number_of_files


def test_length_file_t2p25(get_data_loader_beaktrix: data_type) -> None:
    _, _, energy_densities, magnetizations = get_data_loader_beaktrix
    file_index_t2p25 = 8
    expected_number_of_lines = 3865
    assert len(energy_densities[file_index_t2p25]) == expected_number_of_lines
    assert len(magnetizations[file_index_t2p25]) == expected_number_of_lines


def test_last_line_file_t2p25(get_data_loader_beaktrix: data_type) -> None:
    _, _, energy_densities, magnetizations = get_data_loader_beaktrix
    file_index_t2p25 = 8
    np.testing.assert_almost_equal(energy_densities[file_index_t2p25][-1], -2.84375)
    np.testing.assert_almost_equal(magnetizations[file_index_t2p25][-1], 0.75)


def test_first_line_file_t2p25(get_data_loader_beaktrix: data_type) -> None:
    _, _, energy_densities, magnetizations = get_data_loader_beaktrix
    file_index_t2p25 = 8
    np.testing.assert_almost_equal(energy_densities[file_index_t2p25][0], -3.03125)
    np.testing.assert_almost_equal(magnetizations[file_index_t2p25][0], 0.6796875)
