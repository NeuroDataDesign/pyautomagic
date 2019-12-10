import pytest
from pyautomagic.src.Subject import Subject


def test_extract_name():
    address = 'A\\B\\C\\sub-01'
    expected_name = '01'
    sub = Subject(address)
    name = sub.name
    assert(name == expected_name)


def test_result_folder():
    address = 'A\\B\\C\\sub-01'
    expected_result_folder = 'A\\B\\C\\derivatives\\automagic\\sub-01'
    sub = Subject(address)
    result_folder = sub.result_folder
    assert (result_folder == expected_result_folder)


def test_update_addresses():
    new_data_path = 'a\\b\\c'
    new_project_path = 'x\\y\\z'
    expected_data_folder = 'a\\b\\c\\name'
    expected_project_folder = 'x\\y\\z\\name'
    sub = Subject('A\\B\\C\\name')
    sub.update_addresses(new_data_path, new_project_path)
    result_folder = sub.result_folder
    data_folder = sub.data_folder
    assert(expected_data_folder == data_folder)
    assert(expected_project_folder == result_folder)
