import pytest
import pandas as pd
import os
import pathlib as Path
import sys
sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
from src.format_and_average import file_parser, format_data

test_data_dir = os.path.join(Path.Path(__file__).parent.parent,"test_data")

#test parsed format
#no duplicate configurations
#no negative values for energy?
#check energy and magnetization density to be [-1...1]
#get size?
#(check Energy density is roughly 4 times magnetization density for first ~100 elements at lowest temperature)

def test_parsed():
	df_parsed = file_parser(os.path.join(test_data_dir,"simple_example.txt"))
	df_expected = pd.DataFrame({"m": [0.1,0.4], "E": [0.1,0.4]})
	assert df_parsed.equals(df_expected)

def test_file_parser_checks_duplicates():
	df_parsed = file_parser(os.path.join(test_data_dir,"duplicate_example.txt"))
	df_expected = pd.DataFrame({"m": [0.1,0.4], "E": [0.1,0.4]})
	assert df_parsed.equals(df_expected)

def test_format_data():
	df_input = file_parser(os.path.join(test_data_dir,"format_example.txt"))
	df_expected = pd.DataFrame({"m": [0.1,0.4], "E": [0.1,0.4]})
	df_formatted = format_data(df_input, 64, 256)
	for index, line in df_formatted.iterrows():
		assert -1 <= float(line["m"]) <= 1
		assert -1 <= float(line["E"]) <= 1
	df_formatted = format_data(df_input, 64, -256)
	for index, line in df_formatted.iterrows():
		assert -1 <= float(line["m"]) <= 1
		assert -1 <= float(line["E"]) <= 1



def test_parse_file_name():
	pass