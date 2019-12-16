import pytest
import json
import os
from pyautomagic.src import Project


name = "Dummy project 123456"
d_folder = os.path.join(".", "tests", "test_data", "test_project")
file_ext = ".set"
montage = "biosemi128"
sampling_rate = 5000
params = {'line_freqs' : 0,\
          'filter_type' : 'high', \
          'filt_freq' : None, \
          'filter_length' : 'auto', \
          'eog_regression' : False, \
          'lam' : -1, \
          'tol' : 1e-7, \
          'max_iter': 1000, \
          'interpolation_params': {'line_freqs' : 0,\
                                   'ref_chs': None,\
                                   'reref_chs': None,\
                                   'montage': 'GSN-HydroCel-128'}
          }


def test_data_folder():
    test_Project = Project.Project(
        name, d_folder, file_ext, montage, sampling_rate, params
    )
    expected = os.path.join(".", "tests", "test_data", "test_project")
    assert test_Project.data_folder == expected


def test_results_folder():
    test_Project = Project.Project(
        name, d_folder, file_ext, montage, sampling_rate, params
    )
    assert (
        test_Project.results_folder
        == os.path.join(".", "tests", "test_data", "test_project", "derivatives", "automagic")
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

    assert X.results_folder == os.path.join(".", "tests", "test_data", "test_project", "derivatives", "automagic")

    assert os.path.isfile(
        os.path.join(".", "tests", "test_data", "test_project", "derivatives", "automagic", "Dummy project 123456_results.json")

    )

    assert len(X.block_list) == 2

    with open(os.path.join(".", "tests", "test_data", "test_project", "derivatives", "automagic", "sub-66", "sub-66_task-rest_eeg_results.json"), "r") as jsonFile:
        data = json.load(jsonFile)

    tmp = data["times_committed"]
    data["times_committed"] = 0

    with open(os.path.join(".", "tests", "test_data", "test_project", "derivatives", "automagic", "sub-66", "sub-66_task-rest_eeg_results.json"), "w") as jsonFile:
        json.dump(data, jsonFile)

    os.remove(
        os.path.join(".", "tests", "test_data", "test_project", "derivatives", "automagic", "Dummy project 123456_results.json")
    )

    os.remove(
        os.path.join(".", "tests", "test_data", "test_project", "derivatives", "automagic", "sub-18", "sub-18_task-rest_eeg_raw.fif")
    )
    os.remove(
        os.path.join(".", "tests", "test_data", "test_project", "derivatives", "automagic", "sub-18", "sub-18_task-rest_eeg_results.json")
    )
    os.remove(
        os.path.join(".", "tests", "test_data", "test_project", "derivatives", "automagic", "sub-18", "sub-18_task-rest_eeg.png")
    )
    os.remove(
        os.path.join(".", "tests", "test_data", "test_project", "derivatives", "automagic", "sub-18", "sub-18_task-rest_eeg_orig.png")
    )
