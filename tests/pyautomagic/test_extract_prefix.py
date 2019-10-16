import pytest
from pyautomagic.src.block_methods import extract_prefix

def test_basic_input():
    test_path = '/Documents/myproject/results/subj002/eeg/gip_sess1'
    expected_prefix = 'gip'
    assert(expected_prefix == extract_prefix(test_path))
    
def test_invalid_input():
    prefix_1 = ['nip','np']
    pytest.raises(TypeError,extract_prefix,prefix = prefix_1)
    
def test_invalid_prefix():
    test_path_1 = '/Documents/myproject/results/subj002/eeg/_sess1'
    test_path_2 = '/Documents/myproject/results/subj002/eeg/pp_sess1'
    expected_prefix_1 = ''
    assert(expected_prefix_1 == extract_prefix(test_path_1))
    pytest.raises(ValueError,extract_prefix,result_path = test_path_2)