# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 21:03:04 2025

@author: judith
"""

import os
import sys

import numpy as np
import pytest

sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
from someDefs import calculate_volume
from someDefs import maximum_hkl
from test_data import testdata_maximum_hkl

@pytest.mark.parametrize(("inp", "expected"), testdata_maximum_hkl.testdata)
def test_maximum_hkl(
    inp: tuple[str,float],
    expected: int,
) -> None:
    result: tuple[float] = maximum_hkl(*inp)
    np.testing.assert_allclose(
        result, expected, rtol=1e-7, atol=0.0, equal_nan=False, strict=True
    )