import pandas as pd
import pathlib
from src.file_handler import get_temperature_from_file_name


def load_eggwin(file_path: pathlib.Path) -> pd.DataFrame:
    temperature = get_temperature_from_file_name(file_path.name)
    dataFrame = pd.read_table(
        file_path,
        sep="\\s+",
        comment="#",
        header=None,
        names=["id", "energy_density", "magnetization_density"],
        dtype={"id": int, "energy_density": float, "magnetization_density": float},
    )
    dataFrame["temperature"] = temperature
    return dataFrame


def load_siegfried(file_path: pathlib.Path):
    temperature = get_temperature_from_file_name(file_path.name)
    dataFrame = pd.read_table(
        file_path,
        sep="\\s+",
        header=None,
        names=["dummy", "id", "energy_density", "magnetization_density"],
        dtype={"id": int, "energy_density": float, "magnetization_density": float},
    )
    dataFrame.drop(columns=["dummy"], inplace=True)
    dataFrame["temperature"] = temperature
    return dataFrame


def load_beaktrix(file_path: pathlib.Path):
    temperature = get_temperature_from_file_name(file_path.name)
    dataFrame = pd.read_table(
        file_path,
        sep="\\s+",
        header=None,
        names=["id", "energy_density", "magnetization_density"],
        dtype={"id": int, "energy_density": float, "magnetization_density": float},
    )
    dataFrame["temperature"] = temperature
    return dataFrame
