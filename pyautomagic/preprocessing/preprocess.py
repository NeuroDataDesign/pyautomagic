import mne
import matplotlib.pyplot as plt
import numpy as np

""" preprocess
    Performs all the preprocessing algorithims on the EEG data
    
    Parameters
    ----------
    eeg : mne raw object
        First Parameter, EEG Data (must include)
    params: dict
        dictionary of all the parameters 
        params = {'line_noise' : 50 \
                'filter_type': None, \
                'filt_freq': None, \
                'filter_length': 'auto', \
                'eog_index': -1, \
                'lam': -1,
                'tol': 1e-7,
                'max_iter': 1000
                }
        values included are default 
    
    Returns
    -------
    Data : double numpy array
        Corrected Data
    fig : matlib figures
        Figures of the data at different processing stages        
    
"""
def preprocess(eeg, params):
    
    #performPrep
    badChannels = ['f','s','g']#prep_pipeline(eeg,params['line_noise'])
    eeg.info['bads'] = badChannels
    
    #perfom filter
    eeg_filt = eeg.copy()
    eeg_filt._data = performFilter(eeg.get_data(), eeg.sfreq,\
                             params['filter_type'], \
                             params['filt_freq'],\
                             params['filter_length'])
    
    #eog_regression
    eeg_filt_eog = eeg_filt.copy()
    eeg_filt_eog = performEOGRegression(raw_filt)
    
    #perform RPCA
    eeg_filt_eog_rpca = eeg_filt_eog.copy()
    eeg_filt_eog_rpca._data, noise = performRPCA(raw_filt_eog.get_data(), \
                                    params['lam'], \
                                    params['tol'], \
                                    params['maxIter'])
    
    #Figures 
    
    fig1 = plt.figure(1)
    plt.setp(fig1, color=[1,1,1])
    plt.subplot([11,1,1])
    #EOG Graph
    if 'eeg' in eeg:
        plt.jet()
        eog = raw.pick_types(eog=True)
        scale_min = np.round(np.min(np.min(eog.get_data())))
        scale_max = np.round(np.max(np.max(eog.get_data())))
        plt.clim(scale_min,scale_max)
        plt.title('Filtered EOG data');
        plt.colorbar()
        
   
