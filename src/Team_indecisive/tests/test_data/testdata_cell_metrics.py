from typing import Any

testdata: list[tuple[list[float], dict[str, Any]]] = []

input_0: list[float] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
expected_0: dict[str, float] = {
    "s11": 0.0,
    "s22": 0.0,
    "s33": 0.0,
    "s12": 0.0,
    "s23": 0.0,
    "s13": 0.0,
    "s_min": 0.0,
    "Vsq": 0.0,
    "Volume": 0.0,
}

testdata.append((input_0, expected_0))
