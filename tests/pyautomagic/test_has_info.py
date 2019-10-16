import pytest
from pyautomagic.src.block_methods import has_info

def test_basic_input():
    prefix_1 = 'nip'
    prefix_2 = 'np'
    prefix_3 = ''
    expected_out_1 = True
    expected_out_2 = False
    expected_out_3 = False
    assert(expected_out_1==has_info(prefix_1))
    assert(expected_out_2==has_info(prefix_2))
    assert(expected_out_3==has_info(prefix_3))

def test_incorrect_input():
    prefix_1 = ['nip','np']
    pytest.raises(TypeError,has_info,prefix = prefix_1)