import pytest
import pandas as pd
import os
import pathlib as Path
import sys
sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
from src.format_and_average import file_parser, format_data, get_temp_from_filename, conc_input

test_data_dir = os.path.join(Path.Path(__file__).parent.parent,"test_data")

#test parsed format
#no duplicate configurations
#no negative values for energy?
#check energy and magnetization density to be [-1...1]
#get size?
#(check Energy density is roughly 4 times magnetization density for first ~100 elements at lowest temperature)

eggwin_dict = {"conf":0, "m":1, "E":2}

def test_parsed():
	df_parsed = file_parser(os.path.join(test_data_dir,"simple_example.txt"), eggwin_dict)
	df_expected = pd.DataFrame({"m": [0.1,0.4], "E": [0.1,0.4]})
	assert df_parsed.equals(df_expected)

def test_file_parser_checks_duplicates():
	df_parsed = file_parser(os.path.join(test_data_dir,"duplicate_example.txt"), eggwin_dict)
	df_expected = pd.DataFrame({"m": [0.1,0.4], "E": [0.1,0.4]})
	assert df_parsed.equals(df_expected)

def test_format_data():
	df_input = file_parser(os.path.join(test_data_dir,"format_example.txt"), eggwin_dict)
	df_expected = pd.DataFrame({"m": [0.1,0.4], "E": [0.1,0.4]})
	df_formatted = format_data(df_input, 64, 256)
	for index, line in df_formatted.iterrows():
		assert -1 <= float(line["m"]) <= 1
		assert -1 <= float(line["E"]) <= 1
	df_formatted = format_data(df_input, 64, -256)
	for index, line in df_formatted.iterrows():
		assert -1 <= float(line["m"]) <= 1
		assert -1 <= float(line["E"]) <= 1

def test_get_temp_from_filename():
	file_name = os.path.join(test_data_dir,"Temp1.5.txt")
	assert 1.5 == get_temp_from_filename(file_name)
	file_name = os.path.join(test_data_dir,"T1.54.txt")
	assert 1.54 == get_temp_from_filename(file_name)
	file_name = os.path.join(test_data_dir,"T.54.txt")
	assert 0.54 == get_temp_from_filename(file_name)
	file_name = os.path.join(test_data_dir,"T54.txt")
	assert 54.0 == get_temp_from_filename(file_name)



def test_concatenate():
	df_input = pd.DataFrame({"m": [0.1,0.4], "E": [0.1,0.4]})
	df_output = pd.DataFrame(columns=["T", "m_mean", "E_mean"])
	df_output = conc_input(os.path.join(test_data_dir,"Temp1.5.txt"), pd.DataFrame(columns=["T", "m_mean", "E_mean"]), pd.DataFrame({"m": [0.1,0.4], "E": [0.1,0.4]}))
	df_expected = pd.DataFrame({"T": [1.5], "m_mean": [0.25], "E_mean": [0.25]})
	assert df_output.equals(df_expected)
	df_output = conc_input(os.path.join(test_data_dir,"Temp2.5.txt"), df_output, pd.DataFrame({"m": [0.2,0.5], "E": [0.2,0.5]}))
	df_expected = pd.DataFrame({"T": [1.5, 2.5], "m_mean": [0.25, 0.35], "E_mean": [0.25, 0.35]})
	assert df_output.equals(df_expected)