import numpy as np
import mne
import pytest
import matplotlib.pyplot as plt
from pyautomagic.preprocessing.preprocess import Preprocess


#Test each output type on a sample data set
def test_sample_input_correctType():
    raw = mne.io.read_raw_edf('/Users/raphaelbechtold/Documents/MATLAB/Automagic/automagic/data/Subj1/S001R01.edf')

    params = {'line_noise' : 50, \
              'filter_type' : 'high', \
              'filt_freq' : None, \
              'filter_length' : 'auto', \
              'eog_index' : -1, \
              'lam' : -1,
              'tol' : 1e-7,
              'max_iter': 1000
             }

    preprocess = Preprocess(raw, params)
    eeg,fig1,fig2 = preprocess.fit()
    assert(type(eeg) == mne.io.edf.edf.RawEDF)
    assert(type(fig1) == type(plt.figure()))
    assert(type(fig2) == type(plt.figure()))


#Test each output type on a sample data set 2
def test_sample_input2_correctType():
    raw = mne.io.read_raw_edf('/Users/raphaelbechtold/Documents/MATLAB/Automagic/automagic/data/Subj1/S001R04.edf')

    params = {'line_noise' : 50, \
              'filter_type' : 'high', \
              'filt_freq' : None, \
              'filter_length' : 'auto', \
              'eog_index' : -1, \
              'lam' : -1,
              'tol' : 1e-7,
              'max_iter': 1000
             }


    preprocess = Preprocess(raw, params)
    eeg,fig1,fig2 = preprocess.fit()
    assert(type(eeg) == mne.io.edf.edf.RawEDF)
    assert(type(fig1) == type(plt.figure()))
    assert(type(fig2) == type(plt.figure()))
