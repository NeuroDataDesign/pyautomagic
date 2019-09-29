# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 20:06:37 2019

@author: Vector
"""

import mne
import os
import numpy as np
import matplotlib.pyplot as plt

test_dir = os.path.abspath(os.path.dirname(os.getcwd()))
testdata_dir = os.path.join(test_dir,'test_data','scalp_test.edf')
pyautomagic_dir = os.path.dirname(test_dir)

import sys
sys.path.append(pyautomagic_dir)
from pyautomagic.preprocessing import performFilter

raw = mne.io.read_raw_edf(testdata_dir, preload=True)
#raw.plot()

#Filter data using Hamming windowed sinc FIR filter
EEG_raw = raw._data  #EEG data in ndarray(...,n_times)
sfreq = raw.info['sfreq']  #sampling frequency
times = raw.times  
EEG_lowpass_filt = performFilter.performFilter(EEG_raw, sfreq, 'low')
EEG_highpass_filt = performFilter.performFilter(EEG_raw, sfreq, 'high')
EEG_notch_filt = performFilter.performFilter(EEG_raw, sfreq, 'notch', 60)

fig, axs = plt.subplots(2,figsize=(20,10))
fig.suptitle('Filtering EEG data(Notch)')
axs[0].plot(times, EEG_raw[0])
axs[1].plot(times, EEG_notch_filt[0])
plt.xlabel('time(s)')

plt.figure(figsize=(20,10))
plt.subplot(2,1,1)
plt.specgram(EEG_raw[0],Fs=sfreq)
cb = plt.colorbar()
cb.set_label('PSD Intensity(dB)')
plt.ylabel('Frequency(Hz)')
plt.subplot(2,1,2)
plt.specgram(EEG_notch_filt[0],Fs=sfreq)
cb = plt.colorbar()
cb.set_label('PSD Intensity(dB)')
plt.xlabel('time(s)')
plt.ylabel('Frequency(Hz)')