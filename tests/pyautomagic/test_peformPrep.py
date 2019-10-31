import numpy as np
import mne
import pytest


def test_sample_input():
    data = mne.io.read_raw_edf('/Users/raphaelbechtold/Documents/MATLAB' \
                               '/Automagic/automagic/data/Subj1/S001R04.edf')
    eeg, time = data[:]
    matlab_output = [37,41,43,45]
    badchannels = performPrep(eeg, 0, 160, 50)
    assert(np.array_equal(badchannels,matlab_output))
    
def test_sample_input_change_srate():
    data = mne.io.read_raw_edf('/Users/raphaelbechtold/Documents/MATLAB' \
                               '/Automagic/automagic/data/Subj1/S001R04.edf')
    eeg, time = data[:]
    matlab_output = [41,43,45]
    badchannels = performPrep(eeg, 0, 250, 50)
    assert(np.array_equal(badchannels,matlab_output))
    
def test_sample_input_change_lineNoise():
    data = mne.io.read_raw_edf('/Users/raphaelbechtold/Documents/MATLAB' \
                               '/Automagic/automagic/data/Subj1/S001R04.edf')
    eeg, time = data[:]
    matlab_output = [37,41,43,45]
    badchannels = performPrep(eeg, 0, 160, 60)
    assert(np.array_equal(badchannels,matlab_output))
    
def test_sample_input_change_srate1000():
    data = mne.io.read_raw_edf('/Users/raphaelbechtold/Documents/MATLAB' \
                               '/Automagic/automagic/data/Subj1/S001R04.edf')
    eeg, time = data[:]
    matlab_output = [37,41,43]
    badchannels = performPrep(eeg, 0, 1000, 50)
    assert(np.sum(np.isin(badchannels,matlab_output))==len(matlab_output))
    
def test_detect_constant_values_for_long_time_sample():
    data = mne.io.read_raw_edf('/Users/raphaelbechtold/Documents/MATLAB' \
                               '/Automagic/automagic/data/Subj1/S001R04.edf')
    eeg, time = data[:]
    matlab_output = [4,37,41,43,44,45]
    #input constant value channel
    eeg[4,::] = -np.ones((1,eeg.shape[1]))
    badchannels = performPrep(eeg, 0, 160, 50)
    assert(np.array_equal(badchannels,matlab_output))
    
def test_detect_high_amplitude():
    data = mne.io.read_raw_edf('/Users/raphaelbechtold/Documents/MATLAB' \
                               '/Automagic/automagic/data/Subj1/S001R04.edf')
    eeg, time = data[:]
    matlab_output = [9,37,41,43,45]
    #input constant value channel
    eeg[9,::] = eeg[9,::] * 10
    badchannels = performPrep(eeg, 0, 160, 50)
    assert(np.array_equal(badchannels,matlab_output))

def test_bad_chan_from_deviation():
    data = mne.io.read_raw_edf('/Users/raphaelbechtold/Documents/MATLAB' \
                               '/Automagic/automagic/data/Subj1/S001R04.edf')
    eeg, time = data[:]
    matlab_output = [9,37,41,43,45]
    #input constant value channel
    eeg[9,::] = eeg[9,::]  + eeg[10,::] 
    badchannels = performPrep(eeg, 0, 160, 50)
    assert(np.array_equal(badchannels,matlab_output))


def test_bad_chan_from_deviation_wSrate():
    data = mne.io.read_raw_edf('/Users/raphaelbechtold/Documents/MATLAB' \
                               '/Automagic/automagic/data/Subj1/S001R04.edf')
    eeg, time = data[:]
    matlab_output = [9,41,43,45]
    #input constant value channel
    eeg[9,::] = eeg[9,::]  + eeg[10,::] 
    badchannels = performPrep(eeg, 0, 250, 50)
    assert(np.array_equal(badchannels,matlab_output))

def test_bad_chan_from_sum_of_channels_srate300():
    data = mne.io.read_raw_edf('/Users/raphaelbechtold/Documents/MATLAB' \
                               '/Automagic/automagic/data/Subj1/S001R04.edf')
    eeg, time = data[:]
    matlab_output = [9,41,43]
    #input constant value channel
    eeg[9,::] = eeg[63,::]  + eeg[10,::] 
    badchannels = performPrep(eeg, 0, 300, 50)
    #detect at least same channels as matlab, but also other noisy channels
    assert(np.sum(np.isin(badchannels,matlab_output))==len(matlab_output))

def test_bad_chan_from_sum_of_channels_srate160():
    data = mne.io.read_raw_edf('/Users/raphaelbechtold/Documents/MATLAB' \
                               '/Automagic/automagic/data/Subj1/S001R04.edf')
    eeg, time = data[:]
    matlab_output = [9,41,43]
    #input constant value channel
    eeg[9,::] = eeg[63,::]  + eeg[10,::] 
    badchannels = performPrep(eeg, 0, 300, 50)
    #detect at least same channels as matlab, but also other noisy channels
    assert(np.sum(np.isin(badchannels,matlab_output))==len(matlab_output))    
    
def test_sample_input_subj2():
    data = mne.io.read_raw_edf('/Users/raphaelbechtold/Documents/MATLAB' \
                               '/Automagic/automagic/data/Subj1/S001R04.edf')
    eeg, time = data[:]
    matlab_output = [37,41,43,45]
    badchannels = performPrep(eeg, 0, 160, 50)
    assert(np.array_equal(badchannels,matlab_output))  
    
    