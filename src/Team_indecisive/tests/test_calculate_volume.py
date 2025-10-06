import os
import sys

import pytest

sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
from someDefs import calculate_volume
from test_data import testdata_calculate_volume


@pytest.mark.parametrize(
    ("input", "expected"), testdata_calculate_volume.testdata
)
def test_calculate_volume(
    input,
    expected,
) -> None:
    print(input)
    result = calculate_volume(*input)
    assert result == expected
