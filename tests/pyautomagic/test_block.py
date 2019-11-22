import pytest
import os
import json
from pyautomagic.pyautomagic.src import Block, Project, Subject

root_path = '/tests/test_data/test_project'
config = {'version':1.0}
params = {'interpolation_params':{}}
sampling_rate = 500
visualization_params = {'downsample_rate' : 5}
quality_thresholds = {'overallThresh': 50, 'timeThresh': 25,
                'chanThresh': 25, 'apply_common_avg': True}
rate_cutoffs = {}
dummy_project = Project.Project(root_path,config,params,sampling_rate,
                        visualization_params,quality_thresholds,rate_cutoffs)


def test_result_path():
    sub_name = '18'
    dummy_subject = Subject.Subject(sub_name)
    data_filename = 'sub-18_task-rest_eeg.set'
    test_block = Block.Block(root_path,data_filename,dummy_project,dummy_subject)
    assert(test_block.result_path == '/tests/test_data/test_project/derivatives/automagic/sub-18')
    
def test_no_existing_results_file():
    sub_name = '18'
    dummy_subject = Subject.Subject(sub_name)
    data_filename = 'sub-18_task-rest_eeg.set'
    test_block = Block.Block(root_path,data_filename,dummy_project,dummy_subject)
    assert(test_block.times_committed == -1)
    
def test_existing_results_file():
    sub_name = '66'
    dummy_subject = Subject.Subject(sub_name)
    data_filename = 'sub-66_task-rest_eeg.set'
    test_block = Block.Block(root_path,data_filename,dummy_project,dummy_subject)
    assert(test_block.times_committed == [])
   
def test_preprocess_and_interpolate():
    sub_name = '18'
    dummy_subject = Subject.Subject(sub_name)
    data_filename = 'sub-18_task-rest_eeg.set'
    test_block = Block.Block(root_path,data_filename,dummy_project,dummy_subject)
    results = test_block.preprocess()
    assert(isinstance(results['automagic']['quality_scores'],dict))
    assert(test_block.times_committed == 0)
    assert(os.path.isfile('/tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_raw.fif'))
    assert(os.path.isfile('/tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_results.json'))
    assert(os.path.isfile('/tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg.png'))
    assert(os.path.isfile('/tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_orig.png'))
    assert(os.path.isfile('/tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_raw.fif'))
    test_block.interpolate()
    result_file = '/tests/test_data/project_test/derivatives/automagic/sub-CZ/ses-01/sub-18_task-rest_eeg_results.json'
    with open(result_file) as json_file:
        block = json.load(json_file)
    assert(block.is_interpolated == True)
    os.path.remove('/tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_raw.fif')
    os.path.isfile('/tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_results.json')
    os.path.isfile('/tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg.png')
    os.path.isfile('/tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_orig.png')
    os.path.isfile('/tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_raw.fif')
   