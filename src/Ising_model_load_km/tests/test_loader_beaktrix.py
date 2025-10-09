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

def test_L(get_data_loader_beaktrix: data_type) -> None:
    L, _, _, _ = get_data_loader_beaktrix
    assert L == 16
    
def test_length_temperatures(get_data_loader_beaktrix: data_type) -> None:
    _, temperatures, _, _ = get_data_loader_beaktrix
    assert len(temperatures) == 28
    
def test_length_energy_densities(get_data_loader_beaktrix: data_type) -> None:
    _, _, energy_densities, _ = get_data_loader_beaktrix
    assert len(energy_densities) == 28

def test_length_magnetizations(get_data_loader_beaktrix: data_type) -> None:
    _, _, _, magnetizations = get_data_loader_beaktrix
    assert len(magnetizations) == 28
    
def test_length_fileT2p25(get_data_loader_beaktrix: data_type) -> None:
    _, temperatures, energy_densities, magnetizations = get_data_loader_beaktrix
    file_index_T2p25 = 8
    assert len(energy_densities[file_index_T2p25]) == 3865
    assert len(magnetizations[file_index_T2p25]) == 3865

def test_last_line_fileT2p25(get_data_loader_beaktrix: data_type) -> None:
    _, temperatures, energy_densities, magnetizations = get_data_loader_beaktrix
    file_index_T2p25 = 8
    assert abs(energy_densities[file_index_T2p25][-1] - -2.84375) < 1e-5
    assert abs(magnetizations[file_index_T2p25][-1] - 0.75) < 1e-5

def test_first_line_fileT2p25(get_data_loader_beaktrix: data_type) -> None:
    _, temperatures, energy_densities, magnetizations = get_data_loader_beaktrix
    file_index_T2p25 = 8
    assert abs(energy_densities[file_index_T2p25][0] - -3.03125) < 1e-5
    assert abs(magnetizations[file_index_T2p25][0] - 0.6796875) < 1e-5