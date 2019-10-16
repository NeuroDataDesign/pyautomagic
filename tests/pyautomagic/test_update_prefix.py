import pytest
from pyautomagic.src.block_methods import update_prefix

def test_basic_input():
    is_interpolated, rate, prefix, commitedN = True, 'good','bip',2
    expected_updated_prefix = 'gbiip'
    assert(expected_updated_prefix == update_prefix(is_interpolated, rate, prefix, commitedN))
    is_interpolated, rate, prefix, commitedN = False, 'ok',None,1
    expected_updated_prefix = 'op'
    assert(expected_updated_prefix == update_prefix(is_interpolated, rate, prefix, commitedN))
    
def test_invalid_input():
    is_interpolated, rate, prefix, commitedN = True, 3,'bip','one'
    pytest.raises(Exception,update_prefix,is_interpolated=is_interpolated,rate=rate,prefix=prefix,commitedN=commitedN)
    pytest.raises(Exception,update_prefix)
    