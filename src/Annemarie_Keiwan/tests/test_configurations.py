import tempfile
import pathlib
import numpy as np
from src.Configurations import load_eggwin, load_siegfried, load_beaktrix
import pytest


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield pathlib.Path(temp_dir)


def test_eggwin_configuration_loading(temp_dir: str):
    file_content = """#            conf                E                M
0.00000000e+00   6.40000000e+01   2.56000000e+02
1.00000000e+00   6.40000000e+01   2.56000000e+02
2.00000000e+00   6.40000000e+01   2.56000000e+02
3.00000000e+00   6.40000000e+01   2.56000000e+02
"""
    with open(pathlib.Path(temp_dir, "temp256.0.txt"), "w") as f:
        f.write(file_content)
    dataFrame = load_eggwin(pathlib.Path(temp_dir, "temp256.0.txt"))
    assert dataFrame.shape == (4, 4)
    assert list(dataFrame.columns) == [
        "id",
        "energy_density",
        "magnetization_density",
        "temperature",
    ]
    assert isinstance(dataFrame["id"].iloc[0], np.int64)
    assert dataFrame["id"].iloc[0] == 0
    assert dataFrame["energy_density"].iloc[0] == 64.0
    assert dataFrame["magnetization_density"].iloc[0] == 256.0
    assert dataFrame["temperature"].iloc[0] == 256.0
    assert dataFrame["temperature"].iloc[2] == 256.0
    assert dataFrame["temperature"].iloc[3] == 256.0


def test_siegfried_configuration_loading(temp_dir: str):
    file_content = """8.00000000e-01   0.00000000e+00   4.00000000e+00   1.00000000e+00
8.00000000e-01   1.00000000e+00   4.00000000e+00   1.00000000e+00
8.00000000e-01   2.00000000e+00   4.00000000e+00   1.00000000e+00
8.00000000e-01   3.00000000e+00   4.00000000e+00   1.00000000e+00
"""
    with open(pathlib.Path(temp_dir, "T0.8.txt"), "w") as f:
        f.write(file_content)

    dataFrame = load_siegfried(pathlib.Path(temp_dir, "T0.8.txt"))
    assert dataFrame.shape == (4, 4)
    assert list(dataFrame.columns) == [
        "id",
        "energy_density",
        "magnetization_density",
        "temperature",
    ]
    assert isinstance(dataFrame["id"].iloc[0], np.int64)
    assert dataFrame["id"].iloc[0] == 0
    assert dataFrame["energy_density"].iloc[0] == 4.0
    assert dataFrame["magnetization_density"].iloc[0] == 1.0
    assert dataFrame["temperature"].iloc[0] == 0.8
    assert dataFrame["temperature"].iloc[2] == 0.8
    assert dataFrame["temperature"].iloc[3] == 0.8


def test_beaktrix_configuration_loading(temp_dir: str):
    file_content = """0.00000000e+00  -4.00000000e+00   1.00000000e+00
1.00000000e+00  -4.00000000e+00   1.00000000e+00
2.00000000e+00  -4.00000000e+00   1.00000000e+00
3.00000000e+00  -4.00000000e+00   1.00000000e+00
"""
    with open(pathlib.Path(temp_dir, "T0.5.txt"), "w") as f:
        f.write(file_content)

    dataFrame = load_beaktrix(pathlib.Path(temp_dir, "T0.5.txt"))
    assert dataFrame.shape == (4, 4)
    assert list(dataFrame.columns) == [
        "id",
        "energy_density",
        "magnetization_density",
        "temperature",
    ]
    assert isinstance(dataFrame["id"].iloc[0], np.int64)
    assert dataFrame["id"].iloc[0] == 0
    assert dataFrame["energy_density"].iloc[0] == -4.0
    assert dataFrame["magnetization_density"].iloc[0] == 1.0
    assert dataFrame["temperature"].iloc[0] == 0.5
    assert dataFrame["temperature"].iloc[2] == 0.5
    assert dataFrame["temperature"].iloc[3] == 0.5
