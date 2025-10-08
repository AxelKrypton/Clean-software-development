import numpy as np

testdata: list[tuple[list[float], tuple[np.ndarray, ...]]] = []

input_0: list[float] = [1.0, 1.0, 1.0, 90.0, 90.0, 90.0]
expected_0: tuple[np.ndarray, ...] = (
    np.array([1.0, 0.0, 0.0]),
    np.array([0.0, 1.0, 0.0]),
    np.array([0.0, 0.0, 1.0]),
    np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    ),
)


testdata.append((input_0, expected_0))
