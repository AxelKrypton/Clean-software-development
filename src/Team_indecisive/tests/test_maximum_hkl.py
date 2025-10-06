import os
import sys

import pytest

sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
from someDefs import maximum_hkl
from test_data import testdata_maximum_hkl


@pytest.mark.parametrize(("inp", "expected"), testdata_maximum_hkl.testdata)
def test_maximum_hkl(
    inp: tuple[str, float],
    expected: int,
) -> None:
    result: int = maximum_hkl(*inp)
    assert result == expected
