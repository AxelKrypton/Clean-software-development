import os
import sys
import warnings

import numpy as np
import pytest

sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
from someDefs import reciprocal_vector
from test_data import testdata_reciprocal_vector


input_type = tuple[list[float], list[float], list[float]]
expected_type = tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]


@pytest.mark.parametrize(("inp", "expected", "equal_nan"), testdata_reciprocal_vector.testdata)
def test_reciprocal_vector(inp: input_type, expected: expected_type, equal_nan: bool) -> None:
    if equal_nan:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="divide by zero encountered in scalar divide")
            warnings.filterwarnings("ignore", message="invalid value encountered in multiply")
            with pytest.raises(RuntimeError) as raised_exception:
                result: expected_type = reciprocal_vector(*inp)
        assert "Colinear vectors in reciprocal_vector!" in str(raised_exception)
    else:
        result: expected_type = reciprocal_vector(*inp)
        np.testing.assert_allclose(
            result[:3],
            expected[:3],
            rtol=1e-7,
            atol=0.0,
            equal_nan=equal_nan,
            err_msg="Reciprocal vectors value not matchings",
            strict=True,
        )
        np.testing.assert_allclose(
            result[3],
            expected[3],
            rtol=1e-7,
            atol=0.0,
            equal_nan=equal_nan,
            err_msg="Reciprocal vector base not matchings",
            strict=True,
        )

