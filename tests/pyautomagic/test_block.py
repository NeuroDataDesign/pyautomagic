import pytest
import os
import json
from pyautomagic.src import Block, Project, Subject

root_path = './tests/test_data/test_project'
config = {'version':1.0}
params = {'interpolation_params':{}}
montage = 'biosemi128'
sampling_rate = 500
visualization_params = {'downsample_rate' : 5}
quality_thresholds = {'overall_thresh': 50, 'time_thresh': 25,
                'chan_thresh': 25, 'apply_common_avg': True}
rate_cutoffs = {'overall_Good_Cutoff':0.1,'overall_Bad_Cutoff':0.2,'time_Good_Cutoff':0.1,
                                    'time_Bad_Cutoff':0.2,'bad_Channel_Good_Cutoff':0.15,
                                    'bad_Channel_Bad_Cutoff':0.3,'channel_Good_Cutoff':0.15,
                                    'channel_Bad_Cutoff':0.3}
dummy_project = Project.Project(root_path,config,params,sampling_rate,
                        visualization_params,quality_thresholds,rate_cutoffs,montage)


def test_result_path():
    sub_name = '18'
    dummy_subject = Subject.Subject(sub_name)
    data_filename = 'sub-18_task-rest_eeg.set'
    test_block = Block.Block(root_path,data_filename,dummy_project,dummy_subject)
    assert(test_block.result_path == './tests/test_data/test_project/derivatives/automagic/sub-18')
    
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
    print(test_block.rate)
    assert(test_block.times_committed == 0)
   
def test_preprocess_and_interpolate():
    sub_name = '18'
    dummy_subject = Subject.Subject(sub_name)
    data_filename = 'sub-18_task-rest_eeg.set'
    test_block = Block.Block(root_path,data_filename,dummy_project,dummy_subject)
    results = test_block.preprocess()
    assert(isinstance(results['automagic']['quality_scores'],dict))
    assert(test_block.times_committed == 0)
    assert(os.path.isfile('./tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_raw.fif'))
    assert(os.path.isfile('./tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_results.json'))
    assert(os.path.isfile('./tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg.png'))
    assert(os.path.isfile('./tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_orig.png'))
    #assert(os.path.isfile('./tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_raw.fif'))
    test_block.interpolate()
    result_file = './tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_results.json'
    with open(result_file) as json_file:
        block = json.load(json_file)
    assert(block['is_interpolated'] == True)
    os.remove('./tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_raw.fif')
    os.remove('./tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_results.json')
    os.remove('./tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg.png')
    os.remove('./tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_orig.png')
    #os.path.remove('./tests/test_data/test_project/derivatives/automagic/sub-18/sub-18_task-rest_eeg_raw.fif')
   