import json
import os

import pytest

from pyautomagic.src import Block, Project, Subject

name = "Dummy project 123456"
root_path = os.path.join(".", "tests", "test_data", "test_project")
config = {"version": 1.0,
          "default_params" : {'line_freqs' : 0,\
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

         }
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
montage = "GSN-HydroCel-128"
file_ext = ".set"
sampling_rate = 500
visualization_params = {"downsample_rate": 5}
quality_thresholds = {
    "overall_thresh": 50,
    "time_thresh": 25,
    "chan_thresh": 25,
    "apply_common_avg": True,
}
rate_cutoffs = {
    "overall_Good_Cutoff": 0.1,
    "overall_Bad_Cutoff": 0.2,
    "time_Good_Cutoff": 0.1,
    "time_Bad_Cutoff": 0.2,
    "bad_Channel_Good_Cutoff": 0.15,
    "bad_Channel_Bad_Cutoff": 0.3,
    "channel_Good_Cutoff": 0.15,
    "channel_Bad_Cutoff": 0.3,
}

dummy_project = Project.Project(
    name,
    root_path,
    file_ext,
    montage,
    sampling_rate,
    params
)


def test_result_path():
    sub_name = "18"
    dummy_subject = Subject.Subject(sub_name)
    data_filename = "sub-18_task-rest_eeg.set"
    test_block = Block.Block(root_path, data_filename, dummy_project, dummy_subject)
    assert (
        test_block.result_path
        == os.path.join(".", "tests", "test_data", "test_project", "derivatives", "automagic", "sub-18")
    )


def test_no_existing_results_file():
    sub_name = "18"
    dummy_subject = Subject.Subject(sub_name)
    data_filename = "sub-18_task-rest_eeg.set"
    test_block = Block.Block(root_path, data_filename, dummy_project, dummy_subject)
    assert test_block.times_committed == -1


def test_existing_results_file():
    sub_name = "66"
    dummy_subject = Subject.Subject(sub_name)
    data_filename = "sub-66_task-rest_eeg.set"
    test_block = Block.Block(root_path, data_filename, dummy_project, dummy_subject)
    print(test_block.rate)
    assert test_block.times_committed == 0


def test_preprocess_and_interpolate():
    sub_name = "18"
    dummy_subject = Subject.Subject(sub_name)
    data_filename = "sub-18_task-rest_eeg.set"
    test_block = Block.Block(root_path, data_filename, dummy_project, dummy_subject)
    results = test_block.preprocess()
    assert isinstance(results["automagic"]["quality_scores"], dict)
    assert test_block.times_committed == 0
    assert os.path.isfile(
        os.path.join(".", "tests", "test_data", "test_project", "derivatives", "automagic", "sub-18", "sub-18_task-rest_eeg_raw.fif")
    )
    assert os.path.isfile(
        os.path.join(".", "tests", "test_data", "test_project", "derivatives", "automagic", "sub-18", "sub-18_task-rest_eeg_results.json")
    )
    assert os.path.isfile(
        os.path.join(".", "tests", "test_data", "test_project", "derivatives", "automagic", "sub-18", "sub-18_task-rest_eeg.png")
    )
    assert os.path.isfile(
        os.path.join(".", "tests", "test_data", "test_project", "derivatives", "automagic", "sub-18", "sub-18_task-rest_eeg_orig.png")
    )
    # assert(os.path.isfile('./tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_raw.fif'))
    test_block.interpolate()
    result_file = os.path.join(".", "tests", "test_data", "test_project", "derivatives", "automagic", "sub-18", "sub-18_task-rest_eeg_results.json")
    with open(result_file) as json_file:
        block = json.load(json_file)
    assert block["is_interpolated"] == True
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
    # os.path.remove('./tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_raw.fif')
