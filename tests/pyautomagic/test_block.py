import pytest
import os
from pyautomagic.pyautomagic.src import Block, Project, Subject

root_path = '/tests/test_data/project_test'
config = {'version':1.0}
params = {'interpolation_params':{}}
sampling_rate = 1028
visualization_params = {'downsample_rate' : 5}
quality_thresholds = {'overallThresh': 50, 'timeThresh': 25,
                'chanThresh': 25, 'apply_common_avg': True}
rate_cutoffs = {}
sub_name = 'CZ'


dummy_project = Project.Project(root_path,config,params,sampling_rate,
                        visualization_params,quality_thresholds,rate_cutoffs)
dummy_subject = Subject.Subject(sub_name)


def test_result_path():
    data_filename = 'sub-CZ_ses-02_task-rest_eeg.edf'
    test_block = Block.Block(root_path,data_filename,dummy_project,dummy_subject)
    assert(test_block.result_path == '/tests/test_data/project_test/derivatives/automagic/sub-CZ/ses-02')
    
def test_no_existing_results_file():
    data_filename = 'sub-CZ_ses-02_task-rest_eeg.edf'
    test_block = Block.Block(root_path,data_filename,dummy_project,dummy_subject)
    assert(test_block.times_committed == -1)
    
def test_existing_results_file():
    data_filename = 'sub-CZ_ses-01_task-rest_eeg.edf'
    test_block = Block.Block(root_path,data_filename,dummy_project,dummy_subject)
    assert(test_block.time_committed == [])

def test_loading_data():
    data_filename = 'sub-CZ_ses-01_task-rest_eeg.edf'
    test_block = Block.Block(root_path,data_filename,dummy_project,dummy_subject)
    extracted_data,path = test_block.load_data()
    assert(path == '/tests/test_data/project_test/sub-CZ/ses-01/sub-CZ_ses-02_task-rest_eeg.edf')
    
def test_preprocess():
    data_filename = 'sub-CZ_ses-01_task-rest_eeg.edf'
    test_block = Block.Block(root_path,data_filename,dummy_project,dummy_subject)
    results = test_block.preprocess()
    assert(isinstance(results['automagic']['quality_scores'],dict))
    
    assert(os.path.isfile('/tests/test_data/project_test/derivatives/automagic/sub-CZ/ses-01/sub-CZ_ses-02_task-rest_eeg_raw.fif'))
    assert(os.path.isfile('/tests/test_data/project_test/derivatives/automagic/sub-CZ/ses-01/sub-CZ_ses-02_task-rest_eeg_results.json'))
    assert(os.path.isfile('/tests/test_data/project_test/derivatives/automagic/sub-CZ/ses-01/sub-CZ_ses-02_task-rest_eeg.png'))
    assert(os.path.isfile('/tests/test_data/project_test/derivatives/automagic/sub-CZ/ses-01/sub-CZ_ses-02_task-rest_eeg_orig.png'))
    assert(os.path.isfile('/tests/test_data/project_test/derivatives/automagic/sub-CZ/ses-01/sub-CZ_ses-02_task-rest_eeg_raw.fif'))
    
def test_interpolate():
    data_filename = 'sub-CZ_ses-01_task-rest_eeg.edf'
    test_block = Block.Block(root_path,data_filename,dummy_project,dummy_subject)
    test_block.preprocess()
    test_block.interpolate()
    assert(test_block.is_interpolated == True)