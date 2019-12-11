import pytest
import os
from pyautomagic.src import Project


name = "Dummy project 123456"
d_folder = os.path.join("..", "test_data", "test_dataset_folder")
file_ext = ".edf"
montage = "A"
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
    expected = os.path.join("..", "test_data", "test_dataset_folder")
    assert test_Project.data_folder == expected


def test_results_folder():
    test_Project = Project.Project(
        name, d_folder, file_ext, montage, sampling_rate, params
    )
    assert (
        test_Project.results_folder
        == r"..\test_data\test_dataset_folder\derivatives\automagic"
    )


def test_file_extension():
    test_Project = Project.Project(
        name, d_folder, file_ext, montage, sampling_rate, params
    )
    assert test_Project.file_extension == "edf"


def test_set_montage():
    test_Project = Project.Project(
        name, d_folder, file_ext, montage, sampling_rate, params
    )
    assert test_Project.montage == "A"


def test_sampling_rate():
    test_Project = Project.Project(
        name, d_folder, file_ext, montage, sampling_rate, params
    )
    assert test_Project.sampling_rate == 5000


def test_project_pyautomagic_run():

    open(
        r"..\test_data\test_dataset_folder\sub-001\eeg\sub-001_task-faceFO_eeg.edf", "w"
    )
    open(
        r"..\test_data\test_dataset_folder\sub-002\eeg\sub-002_task-faceFO_eeg.edf", "w"
    )
    open(
        r"..\test_data\test_dataset_folder\sub-003\eeg\sub-003_task-faceFO_eeg.edf", "w"
    )
    open(
        r"..\test_data\test_dataset_folder\sub-004\eeg\sub-004_task-faceFO_eeg.edf", "w"
    )
    open(
        r"..\test_data\test_dataset_folder\sub-005\eeg\sub-005_task-faceFO_eeg.edf", "w"
    )
    open(
        r"..\test_data\test_dataset_folder\sub-006\eeg\sub-006_task-faceFO_eeg.edf", "w"
    )
    open(
        r"..\test_data\test_dataset_folder\sub-007\eeg\sub-007_task-faceFO_eeg.edf", "w"
    )
    open(
        r"..\test_data\test_dataset_folder\sub-008\eeg\sub-008_task-faceFO_eeg.edf", "w"
    )
    open(
        r"..\test_data\test_dataset_folder\sub-009\eeg\sub-009_task-faceFO_eeg.edf", "w"
    )
    open(
        r"..\test_data\test_dataset_folder\sub-010\eeg\sub-010_task-faceFO_eeg.edf", "w"
    )

    X = Project.Project(name, d_folder, file_ext, montage, sampling_rate, params)

    X.preprocess_all()

    X.interpolate_selected()

    assert X.results_folder == r"..\test_data\test_dataset_folder\derivatives\automagic"

    assert os.path.isfile(
        r"..\test_data\test_dataset_folder\derivatives\automagic\Dummy project 123456_results.json"
    )

    assert len(X.block_list) == 10

    assert len(X.interpolate_list) == 10

    assert len(X.already_interpolated) == 10

    os.remove(
        r"..\test_data\test_dataset_folder\derivatives\automagic\Dummy project 123456_results.json"
    )
    os.remove(
        r"..\test_data\test_dataset_folder\sub-001\eeg\sub-001_task-faceFO_eeg.edf"
    )
    os.remove(
        r"..\test_data\test_dataset_folder\sub-002\eeg\sub-002_task-faceFO_eeg.edf"
    )
    os.remove(
        r"..\test_data\test_dataset_folder\sub-003\eeg\sub-003_task-faceFO_eeg.edf"
    )
    os.remove(
        r"..\test_data\test_dataset_folder\sub-004\eeg\sub-004_task-faceFO_eeg.edf"
    )
    os.remove(
        r"..\test_data\test_dataset_folder\sub-005\eeg\sub-005_task-faceFO_eeg.edf"
    )
    os.remove(
        r"..\test_data\test_dataset_folder\sub-006\eeg\sub-006_task-faceFO_eeg.edf"
    )
    os.remove(
        r"..\test_data\test_dataset_folder\sub-007\eeg\sub-007_task-faceFO_eeg.edf"
    )
    os.remove(
        r"..\test_data\test_dataset_folder\sub-008\eeg\sub-008_task-faceFO_eeg.edf"
    )
    os.remove(
        r"..\test_data\test_dataset_folder\sub-009\eeg\sub-009_task-faceFO_eeg.edf"
    )
    os.remove(
        r"..\test_data\test_dataset_folder\sub-010\eeg\sub-010_task-faceFO_eeg.edf"
    )
