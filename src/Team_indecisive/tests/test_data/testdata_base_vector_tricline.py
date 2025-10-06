import numpy as np

testdata: list[list, tuple] = []

inp: list = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
expected: tuple = (np.array([0.0,0.0,0.0]), np.array([0.0,0.0,0.0]), np.array([0.0,0.0,0.0]), np.array([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]))

testdata.append((inp, expected))
