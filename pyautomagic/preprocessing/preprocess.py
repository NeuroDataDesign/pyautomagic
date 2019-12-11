import matplotlib.pyplot as plt
import mne

def preprocess(eeg,params):
    print(eeg.info['ch_names'])
    automagic = {'auto_bad_chans' : [eeg.info['ch_names'][2],eeg.info['ch_names'][4]],
                 'prep':{'performed':True},'filtering':{'performed':True}}
    print(automagic)
    eeg.info['automagic'] = automagic
    fig_1 = plt.figure(figsize=(10,5))
    fig_2 = plt.figure(figsize=(10,5))
    return eeg,fig_1,fig_2
