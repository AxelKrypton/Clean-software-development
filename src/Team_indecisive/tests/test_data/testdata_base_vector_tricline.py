import numpy as np

testdata: list[list, tuple] = []

input_0: list = [1.0, 1.0, 1.0, 90.0, 90.0, 90.0]
expected_0: tuple = (
    np.array([1.0, 0.0, 0.0]),
    np.array([6.123234e-17, 1.000000e00, 0.000000e00]),
    np.array([6.123234e-17, 6.123234e-17, 1.000000e00]),
    np.array(
        [
            [1.000000e00, 6.123234e-17, 6.123234e-17],
            [0.000000e00, 1.000000e00, 6.123234e-17],
            [0.000000e00, 0.000000e00, 1.000000e00],
        ]
    ),
)


testdata.append((input_0, expected_0))
