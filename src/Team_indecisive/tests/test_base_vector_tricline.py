import os
import sys

import pytest

sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
from someDefs import base_vector_tricline
from test_data import testdata_base_vector_tricline


@pytest.mark.parametrize(
    ("input", "expected"), testdata_base_vector_tricline.testdata
)
def test_base_vector_tricline(
    input,
    expected,
) -> None:
    print(input)
    result = base_vector_tricline(*input)
    assert result == expected
