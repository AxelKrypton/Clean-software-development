import numpy as np
import os

testdata: list[tuple[tuple,float]] = []

input_0: tuple = [os.path.join(os.path.dirname(__file__), "../../DATA/SILIZIUM.DAT"),1.5406,30,10]
expected_0: float = -3.6059854189874456e-34

testdata.append((input_0,expected_0))
