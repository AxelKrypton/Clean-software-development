import os
import sys

import numpy as np
import pytest

sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
from src.loader_eggwin import loader_eggwin

# from test_data import testdata_eggwin


# @pytest.mark.parametrize(("inp", "expected"), testdata_eggwin.testdata)
def test_loader_eggwin() -> None:
    loader_eggwin("")
    # np.testing.assert_allclose(
    #     result,
    #     expected,
    #     rtol=1e-7,
    #     atol=1e-14,
    #     equal_nan=False,
    #     strict=True,
    # )
