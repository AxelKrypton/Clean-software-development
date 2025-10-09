from pathlib import Path
import re

_temp_pattern = re.compile(r"^(?:temp|T)(\d+(?:\.\d+)?)\.txt$")


def get_file_paths(folder_path: Path) -> list[Path]:
    assert folder_path.exists(), "Folder does not exist"
    assert folder_path.is_dir(), "Path is not a directory"
    assert len(list(folder_path.iterdir())) != 0, "Directory is empty"
    return list(folder_path.glob("*"))


def get_temperature_from_file_name(filename: str) -> float:
    m = _temp_pattern.match(filename)
    if not m:
        raise ValueError(f"Invalid filename: {filename}")
    return float(m.group(1))
