import pytest
import pandas as pd

from src.format_and_average 

#test parsed format
#no duplicate configurations
#no negative values for energy?
#check energy and magnetization density to be [-1...1]
#get size?
#(check Energy density is roughly 4 times magnetization density for first ~100 elements at lowest temperature)

def test_parsed():
	df_parsed = input_parser("../test_data/simple_example.txt")
	df_expected = pd.DataFrame({"m": [0.1,0.4], "E": [0.1,0.4]})
	df_expected
	assert df_parsed == df_expected