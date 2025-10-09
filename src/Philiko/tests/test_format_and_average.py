import pytest
import pandas as pd
import os
import pathlib as Path
import sys
sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
from src.format_and_average import input_parser

test_data_dir = os.path.join(Path.Path(__file__).parent.parent,"test_data")

#test parsed format
#no duplicate configurations
#no negative values for energy?
#check energy and magnetization density to be [-1...1]
#get size?
#(check Energy density is roughly 4 times magnetization density for first ~100 elements at lowest temperature)

def test_parsed():
	print(test_data_dir)
	df_parsed = input_parser(os.path.join(test_data_dir,"simple_example.txt"))
	df_expected = pd.DataFrame({"m": [0.1,0.4], "E": [0.1,0.4]})
	df_expected
	assert df_parsed == df_expected