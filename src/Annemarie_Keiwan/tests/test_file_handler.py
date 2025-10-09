import tempfile
import pathlib
from typing import List
from itertools import zip_longest
from src.file_handler import get_file_paths, get_temperature_from_file_name


def test_get_file_paths():
    with tempfile.TemporaryDirectory() as source_dir:
        open(pathlib.PurePath(source_dir, "example_1.txt"), "w").close()
        open(pathlib.PurePath(source_dir, "example_2.txt"), "w").close()
        open(pathlib.PurePath(source_dir, "example_3.txt"), "w").close()
        result: List[pathlib.Path] = get_file_paths(pathlib.Path(source_dir))
        assert len(result) == 3
        result_as_strings = [str(path) for path in result]
        result_as_strings.sort()
        reference_strings = [
            str(pathlib.PurePath(source_dir, "example_1.txt")),
            str(pathlib.PurePath(source_dir, "example_2.txt")),
            str(pathlib.PurePath(source_dir, "example_3.txt")),
        ]
        assert result_as_strings[0] == reference_strings[0]
        assert result_as_strings[1] == reference_strings[1]
        assert result_as_strings[2] == reference_strings[2]


def test_get_temperature_from_file_name():
    filenames = [
        "temp2.45.txt",
        "temp2.55.txt",
        "temp2.65.txt",
        "temp3.0.txt",
        "temp3.1.txt",
        "T2.27.txt",
        "T2.55.txt",
        "T2.65.txt",
        "T3.0.txt",
        "T3.1.txt",
        "T3.2.txt",
        "T3.5.txt",
        "T4.1.txt",
    ]
    expected_results = [
        2.45,
        2.55,
        2.65,
        3.0,
        3.1,
        2.27,
        2.55,
        2.65,
        3.0,
        3.1,
        3.2,
        3.5,
        4.1,
    ]
    for filename, expected_result in zip_longest(filenames, expected_results):
        assert isinstance(expected_result, float)
        assert get_temperature_from_file_name(filename) == expected_result
