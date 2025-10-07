import os
import sys

import numpy as np
import pytest

sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
from Kristallite import kristallite
from test_data import testdata_kristallite


@pytest.mark.parametrize(("inp", "expected"), testdata_kristallite.testdata)
def test_crystallite(inp: tuple[str, float, int, int], expected: float) -> None:
    result: float = kristallite(*inp)
    np.testing.assert_allclose(
        result,
        expected,
        rtol=1e-7,
        atol=0.0,
        equal_nan=False,
        err_msg="Crystallite value not matchings",
        strict=True,
    )
