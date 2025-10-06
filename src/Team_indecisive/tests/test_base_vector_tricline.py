import os
import sys

import numpy as np
import pytest

sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
from someDefs import base_vector_tricline
from test_data import testdata_base_vector_tricline


@pytest.mark.parametrize(("inp", "expected"), testdata_base_vector_tricline.testdata)
def test_base_vector_tricline(
    inp: list[float],
    expected: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
) -> None:
    result: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray] = base_vector_tricline(*inp)

    # Check that result and expected have the same structure
    assert len(result) == len(expected), "Result and expected must have same length"

    # Compare each array element-wise
    for r, e in zip(result, expected):
        np.testing.assert_allclose(
            r, e, rtol=1e-7, atol=0.0, equal_nan=False, err_msg="Mismatch in tuple element"
        )