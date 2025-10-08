import os

input_0: tuple[str, float, int, int] = [
    os.path.join(os.path.dirname(__file__), "../../DATA/SILIZIUM.DAT"),
    1.5406,
    30,
    10,
]
expected_0: float = 0.0
testdata = [(input_0, expected_0)]
