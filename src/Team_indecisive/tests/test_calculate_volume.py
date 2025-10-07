import os
import sys

import numpy as np
import pytest

sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
from someDefs import calculate_volume
from test_data import testdata_calculate_volume


@pytest.mark.parametrize(("inp", "expected"), testdata_calculate_volume.testdata)
def test_calculate_volume(
    inp: list[float],
    expected: tuple[float, ...],
) -> None:
    result: tuple[float, ...] = calculate_volume(*inp)
    np.testing.assert_allclose(
        result, expected, rtol=1e-7, atol=0.0, equal_nan=False, strict=True
    )
