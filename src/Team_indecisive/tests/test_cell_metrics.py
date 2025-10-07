import os
import sys

import numpy as np
import pytest

sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
from someDefs import cell_metrics
from test_data import testdata_cell_metrics


@pytest.mark.parametrize(("inp", "expected"), testdata_cell_metrics.testdata)
def test_cell_metrics(
    inp: list[float],
    expected: dict[str, float],
) -> None:
    result: dict[str, float] = cell_metrics(*inp)

    # Check that every expected key matches within tolerance
    for key, val in expected.items():
        np.testing.assert_allclose(
            result[key], val, rtol=1e-7, atol=1e-14, equal_nan=False, strict=True
        )
