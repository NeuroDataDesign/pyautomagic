import pytest
import os
from pyautomagic.src import Project


name = "Dummy project 123456"
d_folder = os.path.join("..", "test_data", "test_project")
file_ext = ".set"
montage = "biosemi128"
sampling_rate = 5000
params = {
    "line_frequencies": 50,
    "filter_type": "high",
    "filt_freq": None,
    "filter_length": "auto",
    "eog_regression": False,
    "lam": -1,
    "tol": 1e-7,
    "max_iter": 1000,
}


def test_data_folder():
    test_Project = Project.Project(
        name, d_folder, file_ext, montage, sampling_rate, params
    )
    expected = os.path.join("..", "test_data", "test_project")
    assert test_Project.data_folder == expected


def test_results_folder():
    test_Project = Project.Project(
        name, d_folder, file_ext, montage, sampling_rate, params
    )
    assert (
        test_Project.results_folder
        == os.path.join("..", "test_data", "test_project", "derivatives", "automagic")
    )


def test_file_extension():
    test_Project = Project.Project(
        name, d_folder, file_ext, montage, sampling_rate, params
    )
    assert test_Project.file_extension == "set"


def test_set_montage():
    test_Project = Project.Project(
        name, d_folder, file_ext, montage, sampling_rate, params
    )
    assert test_Project.montage == "biosemi128"


def test_sampling_rate():
    test_Project = Project.Project(
        name, d_folder, file_ext, montage, sampling_rate, params
    )
    assert test_Project.sampling_rate == 5000


def test_project_pyautomagic_run():

    X = Project.Project(name, d_folder, file_ext, montage, sampling_rate, params)

    X.preprocess_all()

    X.interpolate_selected()

    assert X.results_folder == os.path.join("..", "test_data", "test_project", "derivatives", "automagic")

    assert os.path.isfile(
        os.path.join("..", "test_data", "test_project", "derivatives", "automagic", "Dummy project 123456_results.json")

    )

    assert len(X.block_list) == 2

    assert len(X.interpolate_list) == 2

    assert len(X.already_interpolated) == 2

    os.remove(
        os.path.join("..", "test_data", "test_project", "derivatives", "automagic", "Dummy project 123456_results.json")
    )
