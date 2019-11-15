import matplotlib.pyplot as plt
import mne

def preprocess(eeg,params):
    automagic = {'auto_bad_chans' : [2,3]}
    eeg.info['automagic'] = automagic
    fig_1 = plt.figure(figsize=(10,5))
    fig_2 = plt.figure(figsize=(10,5))
    return eeg,fig_1,fig_2