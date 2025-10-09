
import sys
import os

import pandas as pd 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import two_d_ising_data_format_synchronizer as formatter


folder_path = 'tests/test_data/Eggwin/corrupted_data_conf/'

def test_data_format_synchronizer():
    assert formatter.check_data_folder(folder_path) == []
