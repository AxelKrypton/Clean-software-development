# File for fixtures, we'll see what this'll do

import pytest

@pytest.fixture(scope="session")
def session_data():
	print("	[Setup] Session Data")
	yield {"db_connected": True}
	print("	[Teardown] Function Data")


@pytest.fixture(scope="module")
def module_data():
	print("	[Setup] Module Data")
	yield {"module ready": True}
	print("	[Teardown] Module Data")

@pytest.fixture(scope="function")
def general_password_examples():
	print("	[Setup] Function Data")
	yield {"empty": "", "wrong": "a", "correct": "cd89O+7-VF"}
	print("	[Teardown] Function Data")