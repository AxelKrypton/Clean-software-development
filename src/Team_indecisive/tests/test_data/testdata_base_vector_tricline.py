import numpy as np

testdata: list[tuple[list[float], tuple[np.ndarray]]] = []

input_0: list[float] = [1.0, 1.0, 1.0, 90.0, 90.0, 90.0]
expected_0: tuple[np.ndarray] = (
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
