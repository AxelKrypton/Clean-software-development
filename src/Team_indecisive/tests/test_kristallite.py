import os
import sys
import numpy as np

import pytest
from math import isclose

sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
from Kristallite import crystallite
from test_data import testdata_crystallite

@pytest.mark.parametrize(("inp","expected"),testdata_crystallite.testdata)
def test_crystallite(
        inp:tuple,
        expected:float
        )-> None:
    result: float = crystallite(*inp)
    np.testing.assert_allclose(result, expected, rtol=1e-7,atol=0.0, 
                               equal_nan=False,err_msg="Mismatch in tuple element",
                               strict=True)
    
