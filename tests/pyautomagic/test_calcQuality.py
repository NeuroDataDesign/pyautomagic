import numpy as np
import pytest
from pyautomagic.src.calcQuality import calcQuality
"""

"""

def test_basic_input():
    time = np.arange(.001,.1,.001)
    EEG = np.array(100*np.sin(50*time),10*np.cos(40*time))
    bad_chans = [2]
    expected_quality = {'overall_high_amp': 0, 'times_high_var': .7475, 'ratio_bad_chans': .5, 'chan_high_var': 1, 'mean_abs_volt': 30.6472,
                           'overallThresh': 50, 'timeThresh': 25, 'chanThresh': 25, 'apply_common_avg': True}
    calculated_quality = calcQuality(EEG,bad_chans)
    assert(expected_quality['overall_high_amp']==calculated_quality['overall_high_amp'])
    assert(expected_quality['times_high_var']==calculated_quality['times_high_var'])
    assert(expected_quality['ratio_bad_chans']==calculated_quality['ratio_bad_chans'])
    assert(expected_quality['chan_high_var']==calculated_quality['chan_high_var'])
    assert(expected_quality['mean_abs_volt']==calculated_quality['mean_abs_volt'])
    assert(expected_quality['overallThresh']==calculated_quality['overallThresh'])
    assert(expected_quality['timeThresh']==calculated_quality['timeThresh'])
    assert(expected_quality['chanThresh']==calculated_quality['chanThresh'])
    assert(expected_quality['apply_common_avg']==calculated_quality['apply_common_avg'])
    
    
def test_not_enough_inputs():
    with pytest.raises(TypeError):
        calculated_quality = calcQuality()
        
def test_incorrect_param_type():
    EEG = np.array([1,2,3,4],[10,100,1,40])
    bad_chans = [2]
    overallThresh = True
    chanThresh = 'test'
    timeThresh = False
    avg_ref = 'off'
    calculated_quality = calcQuality(EEG,bad_chans,overallThresh,timeThresh,chanThresh,avg_ref)
    assert(calculated_quality['overallThresh']==50)
    assert(calculated_quality['timeThresh']==25)
    assert(calculated_quality['chanThresh']==25)
    assert(calculated_quality['apply_common_avg']==True)
    
def test_parameters():
    overallThresh = 20
    chanThresh = 20
    timeThresh = 20
    avg_ref = False
    time = np.arange(.001,.1,.001)
    EEG = np.array(100*np.sin(50*time),10*np.cos(40*time))
    bad_chans = [2]
    expected_quality = {'overall_high_amp': 0.4394, 'times_high_var': .8081, 'ratio_bad_chans': .5, 'chan_high_var': .5, 'mean_abs_volt': 36.3618,
                           'overallThresh': 20, 'timeThresh': 20, 'chanThresh': 20,'apply_common_avg': False}
    calculated_quality = calcQuality(EEG,bad_chans,overallThresh,timeThresh,chanThresh,avg_ref)
    assert(expected_quality['overall_high_amp']==calculated_quality['overall_high_amp'])
    assert(expected_quality['times_high_var']==calculated_quality['times_high_var'])
    assert(expected_quality['ratio_bad_chans']==calculated_quality['ratio_bad_chans'])
    assert(expected_quality['chan_high_var']==calculated_quality['chan_high_var'])
    assert(expected_quality['mean_abs_volt']==calculated_quality['mean_abs_volt'])
    assert(expected_quality['overallThresh']==calculated_quality['overallThresh'])
    assert(expected_quality['timeThresh']==calculated_quality['timeThresh'])
    assert(expected_quality['chanThresh']==calculated_quality['chanThresh'])
    assert(expected_quality['apply_common_avg']==calculated_quality['apply_common_avg'])