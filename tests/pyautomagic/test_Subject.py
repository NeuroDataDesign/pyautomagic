import pytest
import os.path
from pyautomagic.src.Subject import Subject


def test_extract_name():
    address = os.path.join("A", "B", "C", "sub-01")
    expected_name = "01"
    sub = Subject(address)
    name = sub.name
    assert name == expected_name


def test_result_folder():
    address = os.path.join("A", "B", "C", "sub-01")
    expected_result_folder = os.path.join(
        "A", "B", "C", "derivatives", "automagic", "sub-01"
    )
    sub = Subject(address)
    result_folder = sub.result_folder
    assert result_folder == expected_result_folder


def test_update_addresses():
    new_data_path = os.path.join("a", "b", "c")
    new_project_path = os.path.join("x", "y", "z")
    expected_data_folder = os.path.join("a", "b", "c", "name")
    expected_project_folder = os.path.join("x", "y", "z", "name")
    sub = Subject("A/B/C/name")
    sub.update_addresses(new_data_path, new_project_path)
    result_folder = sub.result_folder
    data_folder = sub.data_folder
    assert expected_data_folder == data_folder
    assert expected_project_folder == result_folder
