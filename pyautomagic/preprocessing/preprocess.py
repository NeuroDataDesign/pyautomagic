import mne
import matplotlib.pyplot as plt
import numpy as np
from .rpca import rpca
from .performFilter import performFilter
from .perform_EOG_regression import perform_EOG_regression
from .prep.prep_pipeline import prep_pipeline


""" Preprocess
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

class Preprocess:

    def __init__(self,eeg,params):
        eeg.load_data()
        self.eeg = eeg
        self.eog = None
        self.bad_chs = None
        self.params = params
        self.index = 0
        self.filtered = eeg.copy()
        self.eeg_filt_eog = None
        self.eeg_filt_eog_rpca = None
        self.pyautomagic = {'perform_prep' : False,\
                          'perform_filter' : False, \
                          'perform_eog_regression' : False, \
                          'perform_RPCA' : False}
        self.fig1 = None
        self.fig2 = None

        #Return noisy channels found using the prep_pipline()
    def perform_prep(self):
        self.pyautomagic['perform_prep'] = True
        chans = self.eeg.info['ch_names']
        self.bad_chs = chans[4:5]+chans[30:32]+[chans[50]]
        return self.bad_chs #prep_pipeline(self.eeg, self.params)

    #Filter data
    def perform_filter(self):
        self.pyautomagic['perform_filter'] = True
        return performFilter(self.filtered.get_data(), self.eeg.info['sfreq'],\
                                             self.params['filter_type'], \
                                             self.params['filt_freq'],\
                                             self.params['filter_length'])
    #remove artifact from EOG
    def perform_eog_regression(self):
        if ('eog' in self.filtered):
            eeg = self.filtered.copy()
            self.eog = self.filtered.copy()
            if (self.params['eog_regression'] == True):
                self.pyautomagic['perform_eog_regression'] = True
            else:
                self.pyautomagic['perform_eog_regression'] = False
            eeg.pick_types(eeg=True)
            self.eog.pick_types(eog=True)
            self.filtered._data = perform_EOG_regression(eeg.get_data(),self.eog.get_data())
        return self.filtered

    #clean data using rpca
    def perform_RPCA(self):
        self.pyautomagic['perform_RPCA'] = True
        return rpca(self.eeg_filt_eog._data, \
                    self.params['lam'], \
                    self.params['tol'], \
                    self.params['max_iter'])

    #Return figures of the data
    def plot(self):
        self.fig1 = plt.figure(1,frameon=False)
        plt.setp(self.fig1,facecolor=[1,1,1], figwidth=15, figheight=50)
        ax = self.fig1.add_subplot(8, 1, 1)
        #EOG Graph
        if 'eog' in self.filtered:
            data = self.eog._data
            scale_min = np.min(np.min(data))
            scale_max = np.max(np.max(data))
            data = data - ((scale_max + scale_min)/2)
            plt.imshow(data,aspect='auto',extent=[0,(data.shape[1]/self.eeg.info['sfreq']),self.eog.info['nchan'],0],cmap=plt.get_cmap('coolwarm'))
            plt.title('Filtered EOG data')
            plt.colorbar()
        else:
            plt.title('No EOG data available')
            self.params['eog_regression'] = False

        #EEG Filtered Plot
        ax = self.fig1.add_subplot(8, 1, 2)
        data = self.filtered._data
        scale_min = np.min(np.min(data))
        scale_max = np.max(np.max(data))
        data = data - ((scale_max + scale_min)/2)
        plt.imshow(data,aspect='auto',extent=[0,(data.shape[1]/self.eeg.info['sfreq']),self.eeg.info['nchan'],0],cmap=plt.get_cmap('coolwarm'))
        #plt.clim(scale_min,scale_max)
        plt.colorbar()
        plt.title('Filtered EEG data')

        #EEG Filtered Plot Without Bad Channels
        allchan = raw.info['ch_names']
        ax = self.fig1.add_subplot(8, 1, 3)
        #delete this next line (index) when performPrep is fully functional
        self.index = np.array([4,12,18,19,20,21,30,31,32,41,42,44,45,46,47])

        data = self.filtered._data
        scale_min = np.min(np.min(data))
        scale_max = np.max(np.max(data))

        for i in range(len(self.index)): #len(badChannels)
            #index[i] = allchan.index(badChannels[i])
            data[(self.index[i]-1),:] = scale_min * np.ones((self.eeg._data.shape[1]))
        data = data - ((scale_max + scale_min)/2)
        plt.imshow(data,aspect='auto',extent=[0,(data.shape[1]/self.eeg.info['sfreq']),self.eeg.info['nchan'],0],cmap=plt.get_cmap('coolwarm'))
        #plt.clim(scale_min,scale_max)
        plt.title('Detected bad channels')
        plt.colorbar()



        # Plot with EOG regression
        ax = self.fig1.add_subplot(8, 1, 4)

        if self.params['eog_regression']:
            data = self.eog._data
            data = np.delete(data, (self.index-1),0)
            scale_min = np.min(np.min(data))
            scale_max = np.max(np.max(data))
            data = data - ((scale_max + scale_min)/2)
            plt.imshow(data,aspect='auto',extent=[0,(data.shape[1]/self.eeg.info['sfreq']),self.eeg.info['nchan'],0],cmap=plt.get_cmap('coolwarm'))
            #plt.clim(scale_min,scale_max)
            plt.colorbar()
            plt.title('EOG regressed out')
        else:
            plt.title('No EOG-Regression requested')

        #RPCA Corrected Data Plot
        ax = self.fig1.add_subplot(8, 1, 5)
        data = self.eeg_filt_eog_rpca._data
        data = np.delete(data,(self.index-1),0)
        rows = data.shape[0]
        scale_min = np.min(np.min(data))
        scale_max = np.max(np.max(data))
        data = data - ((scale_max + scale_min)/2)
        plt.imshow(data,aspect='auto',extent=[0,(data.shape[1]/self.eeg.info['sfreq']),self.eeg.info['nchan'],0],cmap=plt.get_cmap('coolwarm'))
        #plt.clim(scale_min,scale_max)
        plt.colorbar()
        plt.title('RPCA Corrected EEG data')

        #RPCA Noisy Data Plot
        ax = self.fig1.add_subplot(8, 1, 6)
        noise = np.delete(self.noise, (self.index-1),0)
        scale_min = np.min(np.min(self.noise))
        scale_max = np.max(np.max(self.noise))
        self.noise = self.noise - ((scale_max + scale_min)/2)
        plt.imshow(self.noise,aspect='auto',extent=[0,(data.shape[1]/self.eeg.info['sfreq']),self.eeg.info['nchan'],0],cmap=plt.get_cmap('coolwarm'))
        #plt.clim(scale_min,scale_max)
        plt.colorbar()
        plt.title('Noise')

        eeg_clean = self.eeg_filt_eog_rpca.copy()

        self.fig2 = plt.figure(2)
        plt.setp(self.fig2,facecolor=[1,1,1], figwidth=15)
        data2 = eeg_clean._data
        data2 = np.delete(data2, (self.index-1),0)
        scale_min = np.min(np.min(data2))
        scale_max = np.max(np.max(data2))
        data2 = data2 - ((scale_max + scale_min)/2)
        plt.imshow(data2,aspect='auto',extent=[0,(data2.shape[1]/self.eeg.info['sfreq']),self.eeg.info['nchan'],0],cmap=plt.get_cmap('coolwarm'))
        #plt.clim(scale_min,scale_max)
        plt.colorbar()
        plt.title('Filtered EEG data')



        return self.fig1,self.fig2

    def fit(self):
        #performPrep
        self.eeg.info['bads'] = self.perform_prep()
        self.index = np.zeros(len(self.eeg.info['bads'])).astype(int)

        #perfom filter
        self.filtered._data = self.perform_filter()

        #eog_regression
        self.eeg_filt_eog = self.filtered.copy()
        self.eeg_filt_eog = self.perform_eog_regression()

        #perform RPCA
        self.eeg_filt_eog_rpca = self.eeg_filt_eog.copy()
        self.eeg_filt_eog_rpca._data, self.noise = self.perform_RPCA()

        self.fig1, self.fig2 = self.plot()

        return self.eeg_filt_eog_rpca, self.fig1, self.fig2

