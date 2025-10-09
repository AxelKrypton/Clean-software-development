import os
import sys

import numpy as np
import pytest

sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
from src.loader_siegfried import loader_siegfried

data_type = tuple[int, list[float], list[np.ndarray], list[np.ndarray]]


@pytest.fixture(scope="module")
def get_data_loader_siegfried() -> data_type:
    return loader_siegfried()


def test_loader_siegfried_lattice_size(get_data_loader_siegfried: data_type) -> None:
    l_out, _, _, _ = get_data_loader_siegfried
    expected_lattice_size: int = 32
    assert l_out == expected_lattice_size


def test_loader_siegfried_num_files(get_data_loader_siegfried: data_type) -> None:
    _, temp, energy_density, magnetization = get_data_loader_siegfried
    expected_num_files = 27
    assert len(temp) == expected_num_files
    assert len(energy_density) == expected_num_files
    assert len(magnetization) == expected_num_files


def test_loader_siegfried_check_shapes(get_data_loader_siegfried: data_type) -> None:
    _, _, energy_density, magnetization = get_data_loader_siegfried
    for ed, mag in zip(energy_density, magnetization, strict=True):
        assert ed.shape == mag.shape


def test_loader_siegfried_check_nan_temp(get_data_loader_siegfried: data_type) -> None:
    _, temperatures, _, _ = get_data_loader_siegfried
    assert not np.isnan(temperatures).any()


def test_loader_siegfried_check_nan_ed(get_data_loader_siegfried: data_type) -> None:
    _, _, energy_densities, _ = get_data_loader_siegfried
    for ed in energy_densities:
        assert not np.isnan(ed).any()


def test_loader_siegfried_check_nan_mag(get_data_loader_siegfried: data_type) -> None:
    _, _, _, magnetizations = get_data_loader_siegfried
    for mag in magnetizations:
        assert not np.isnan(mag).any()


def test_loader_siegfried_check_greater_zero_temp(
    get_data_loader_siegfried: data_type,
) -> None:
    _, temperatures, _, _ = get_data_loader_siegfried
    assert np.greater_equal(temperatures, 0.0).all()


def test_loader_siegfried_check_greater_zero_ed(
    get_data_loader_siegfried: data_type,
) -> None:
    _, _, energy_densities, _ = get_data_loader_siegfried
    for ed in energy_densities:
        assert np.greater_equal(ed, 0.0).all()


def test_loader_siegfried_check_greater_zero_mag(
    get_data_loader_siegfried: data_type,
) -> None:
    _, _, _, magnetizations = get_data_loader_siegfried
    for mag in magnetizations:
        assert np.greater_equal(mag, 0.0).all()
