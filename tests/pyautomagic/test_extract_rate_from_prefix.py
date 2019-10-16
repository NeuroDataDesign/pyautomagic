import pytest
from pyautomagic.src.block_methods import extract_rate_from_prefix

def test_basic_input():
    prefix_1 = 'nip'
    prefix_2 = 'gp'
    prefix_3 = ''
    prefix_4 = 'oiip'
    prefix_5 = 'boip'
    expected_out_1 = 'not_rated'
    expected_out_2 = 'good'
    expected_out_3 = 'not_rated'
    expected_out_4 = 'ok'
    expected_out_5 = 'bad'
    assert(expected_out_1==extract_rate_from_prefix(prefix_1))
    assert(expected_out_2==extract_rate_from_prefix(prefix_2))
    assert(expected_out_3==extract_rate_from_prefix(prefix_3))
    assert(expected_out_4==extract_rate_from_prefix(prefix_4))
    assert(expected_out_5==extract_rate_from_prefix(prefix_5))

def test_incorrect_input():
    prefix_1 = ['nip','np']
    pytest.raises(TypeError,extract_rate_from_prefix,prefix = prefix_1)