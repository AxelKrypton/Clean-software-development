import os

testdata: list[list[float], tuple[float]] = []

input_0: tuple[str,float] = ((os.path.join(os.path.dirname(__file__),'..', "../DATA/SILIZIUM.DAT")),1.54)
expected_0: int = (7)

testdata.append((input_0, expected_0))
