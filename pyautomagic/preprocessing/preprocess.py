import mne
import matplotlib.pyplot as plt
import numpy as np
from pyautomagic.preprocessing.rpca import rpca
from pyautomagic.preprocessing.performFilter import performFilter
from pyautomagic.preprocessing.perform_EOG_regression import perform_EOG_regression
from pyprep.prep_pipeline import PrepPipeline

class Preprocess:

    def __init__(self,eeg,params):
        eeg.load_data()
        eeg.rename_channels(lambda s: s.strip("."))
        self.eeg = eeg
        self.eog = None
        self.bad_chs = None
        self.params = params
        self.index = 0
        self.filtered = eeg.copy()
        self.eeg_filt_eog = None
        self.eeg_filt_eog_rpca = None
        self.noise = eeg.copy()
        self.automagic = {'prep': {'performed': False},\
                          'filtering': {'performed': False},\
                          'perform_eog_regression' : False,\
                          'perform_RPCA' : False}

        self.fig1 = None
        self.fig2 = None

        #Return noisy channels found using the prep_pipline()
    def perform_prep(self):
        self.automagic['prep']['performed'] = True
        prep = PrepPipeline(self.eeg, self.params['interpolation_params'],\
            montage_kind=self.params['interpolation_params']['montage'])
        prep = prep.fit()
        self.bad_chs = prep.still_noisy_channels
        self.automagic.update({'auto_bad_chans' : self.bad_chs})
        return self.bad_chs

    #Filter data
    def perform_filter(self):
        self.automagic['filtering']['performed'] = True
        self.filtered._data = performFilter(self.filtered.get_data(), \
                                            self.eeg.info['sfreq'], \
                                            self.params['filter_type'], \
                                            self.params['filt_freq'], \
                                            self.params['filter_length'])
        return self.filtered

    #remove artifact from EOG
    def perform_eog_regression(self):
        self.eeg_filt_eog = self.filtered.copy()
        if ('eog' in self.filtered):
            eeg = self.filtered.copy()
            self.eog = self.filtered.copy()
            if (self.params['eog_regression'] == True):
                self.automagic['perform_eog_regression'] = True
            else:
                self.automagic['perform_eog_regression'] = False
            eeg_indices = eeg.pick_types(eeg=True)
            eog_indices = self.eog.pick_types(eog=True)
            self.eeg_filt_eog._data = perform_EOG_regression(eeg.get_data(eeg_indices),self.eog.get_data(eog_indices))
        return self.eeg_filt_eog

    #clean data using rpca
    def perform_RPCA(self):
        self.eeg_filt_eog_rpca = self.eeg_filt_eog.copy()
        self.eeg_filt_eog_rpca.load_data()
        self.automagic['perform_RPCA'] = True
        self.eeg_filt_eog_rpca._data, self.noise._data = rpca(self.eeg_filt_eog.get_data(), \
                                                              self.params['lam'], \
                                                              self.params['tol'], \
                                                              self.params['max_iter'])
        return self.eeg_filt_eog_rpca._data, self.noise._data

    #Return figures of the data
    def plot(self,show=True):

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
        plt.colorbar()
        plt.title('Filtered EEG data')

        #EEG Filtered Plot Without Bad Channels
        allchan = self.eeg.info['ch_names']
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
        plt.colorbar()
        plt.title('RPCA Corrected EEG data')

        #RPCA Noisy Data Plot
        self.noise = self.eeg_filt_eog_rpca.copy()
        ax = self.fig1.add_subplot(8, 1, 6)
        self.noise._data = np.delete(self.noise._data, (self.index-1),0)
        scale_min = np.min(np.min(self.noise._data))
        scale_max = np.max(np.max(self.noise._data))
        self.noise._data = self.noise._data - ((scale_max + scale_min)/2)
        plt.imshow(self.noise._data,aspect='auto',extent=[0,(data.shape[1]/self.eeg.info['sfreq']),self.eeg.info['nchan'],0],cmap=plt.get_cmap('coolwarm'))
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
        plt.colorbar()
        plt.title('Filtered EEG data')

        if (not show):
            plt.close('all')

        return self.fig1,self.fig2

    def fit(self):

        #performPrep
        if (self.automagic['prep']['performed'] == False):
            print('prep')
            self.eeg.info['bads'] = self.perform_prep()
            self.index = np.zeros(len(self.eeg.info['bads'])).astype(int)

        #perfom filter
        if (self.automagic['filtering']['performed'] == False):
            print('filter')
            self.filtered = self.perform_filter()


        #eog_regression
        if (self.automagic['perform_eog_regression'] == False):
            print('eog_regression')
            self.eeg_filt_eog = self.filtered.copy()
            self.eeg_filt_eog = self.perform_eog_regression()


        #perform RPCA
        if (self.automagic['perform_RPCA'] == False):
            print('rpca')
            self.eeg_filt_eog_rpca = self.eeg_filt_eog.copy()
            self.eeg_filt_eog_rpca._data, self.noise = self.perform_RPCA()

        self.fig1, self.fig2 = self.plot()

        return self.eeg_filt_eog_rpca, self.fig1, self.fig2


