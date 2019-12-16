import matplotlib.pyplot as plt
import mne
import numpy as np
import pytest

from pyautomagic.preprocessing.preprocess import Preprocess


#Test each output type on a sample data set
def test_sample_input_correctType():
    raw = mne.io.read_raw_edf('./tests/test_data/S001R01.edf')
    raw.rename_channels(lambda s: s.strip("."))
    raw.rename_channels(lambda s: s.replace("c", "C").replace("o", "O").\
      replace("f", "F").replace("t", "T").replace("Tp", "TP").replace("Cp", "CP"))
    print(raw.ch_names)
    params = {'line_freqs' : 50,\
              'filter_type' : 'high', \
              'filt_freq' : None, \
              'filter_length' : 'auto', \
              'eog_regression' : False, \
              'lam' : -1, \
              'tol' : 1e-7, \
              'max_iter': 1000, \
              'interpolation_params': {'line_freqs' : raw.info['sfreq'],\
                                       'ref_chs': raw.ch_names,\
                                       'reref_chs': raw.ch_names,\
                                       'montage': 'standard_1020'}
              }

    preprocess = Preprocess(raw, params)
    eeg,fig1,fig2 = preprocess.fit()
    assert(type(eeg) == mne.io.edf.edf.RawEDF)
    assert(type(fig1) == type(plt.figure()))
    assert(type(fig2) == type(plt.figure()))


#Test each output type on a sample data set 2
def test_sample_input2_correctType():
    raw = mne.io.read_raw_edf('./tests/test_data/S001R01.edf')
    raw.rename_channels(lambda s: s.strip("."))
    raw.rename_channels(lambda s: s.replace("c", "C").replace("o", "O").\
      replace("f", "F").replace("t", "T").replace("Tp", "TP").replace("Cp", "CP"))
    params = {'line_freqs' : 50,\
              'filter_type' : 'high', \
              'filt_freq' : None, \
              'filter_length' : 'auto', \
              'eog_regression' : False, \
              'lam' : -1, \
              'tol' : 1e-7, \
              'max_iter': 1000, \
              'interpolation_params': {'line_freqs' : raw.info['sfreq'],\
                                       'ref_chs': raw.ch_names,\
                                       'reref_chs': raw.ch_names,\
                                       'montage': 'standard_1020'}
              }
    preprocess = Preprocess(raw, params)
    eeg,fig1,fig2 = preprocess.fit()
    assert(type(eeg) == mne.io.edf.edf.RawEDF)
    assert(type(fig1) == type(plt.figure()))
    assert(type(fig2) == type(plt.figure()))
