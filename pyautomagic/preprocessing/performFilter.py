# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 20:42:02 2019

@author: Vector
"""
import mne
import numpy as np

def performFilter(EEG, sfreq, filter_type=None, cutoff_freq=None, filter_length='auto'):
    """This function filters EEG data using Hamming windowed sinc FIR filter
    with input filter type and parameters.
    Inputs: 
        EEG                 -ndarray, shape (…, n_times)
        sfreq               -sample frequency
        filter_type         -filter types, can only take 'low', 'high' or 'notch'
        cutoff_freq         -cut-off frequency of filter(Hz)
        filter_length       -Length of the FIR filter to use
        
    Outputs:
        The filtered data  -ndarray, shape (…, n_times)"""
    if filter_type is None:
        print('No Filter Will be Performed')
        if cutoff_freq is not None:
            print('Warning: Unused filter parameter cutoff_freq')
    elif filter_type not in ('low', 'high', 'notch'):
        print("Error input format: filter_type must be 'low', 'high' or 'notch'")
    else:
        if filter_type == 'low':
            if cutoff_freq is None:
                print('Warning: cutoff freq is not given but is required. Default parameters' 
                              'for low pass filtering will be used')
                cutoff_freq = 30    #Default
            EEG_filt = mne.filter.filter_data(EEG, sfreq, None, cutoff_freq, 
                                  picks=None, filter_length=filter_length, l_trans_bandwidth='auto', 
                                  h_trans_bandwidth='auto', n_jobs=1, method='fir', 
                                  phase='zero', fir_window='hamming', 
                                  fir_design='firwin', pad='reflect_limited', verbose=None)
        if filter_type == 'high':
            if cutoff_freq is None:
                print('Warning: cutoff freq is not given but is required. Default parameters'  
                              'for high pass filtering will be used')
                cutoff_freq = 0.5    #Default
            EEG_filt = mne.filter.filter_data(EEG, sfreq, cutoff_freq, None, 
                                  picks=None, filter_length=filter_length, l_trans_bandwidth='auto', 
                                  h_trans_bandwidth='auto', n_jobs=1, method='fir', 
                                  phase='zero', fir_window='hamming', 
                                  fir_design='firwin', pad='reflect_limited', verbose=None)
        if filter_type == 'notch':
            if cutoff_freq is None:
                print('Warning: cutoff freq for notch filter is not complete.'
                              'The default will be used.')
                cutoff_freq = 50    #Default
            EEG_filt = mne.filter.notch_filter(EEG, sfreq, cutoff_freq, 
                                  filter_length=filter_length, notch_widths=None, trans_bandwidth=1, 
                                  method='fir', phase='zero', fir_window='hamming', fir_design='firwin', 
                                  pad='reflect_limited', verbose=None)
    return EEG_filt
            
                
        