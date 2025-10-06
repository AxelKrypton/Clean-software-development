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


def test_maximum_hkl(
    datdatei= os.path.join(os.path.dirname(__file__), "../DATA/SILIZIUM.DAT"),
    lambda_=1.54
) -> None:
    result: tuple[float] = maximum_hkl(datdatei,lambda_)
    expected=7
    result==7
