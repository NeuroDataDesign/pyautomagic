import numpy as np


def performEOGRegression(eeg, eog):

    """clean_eeg = performEOGRegression(eeg,eog)
        performs linear regression to remove eog artifacts from eeg data
        INPUT: eeg, eog data matrices
        OUTPUT: clean_eeg matrix """

    size_eeg = np.shape(eeg)
    size_eog = np.shape(eog)
    if size_eeg == 0 or size_eeg == 0:  # check if the inputs values for eeg and eog are null
        return;

    dimension = len(size_eog)
    if dimension == 1:
        eog.resize((1, size_eog[0]))    # resizing the EOG array so that its pseudoinverse can be calculated
    eeg_t = np.transpose(eeg)
    eog_t = np.transpose(eog)
    pseudoinv = np.linalg.pinv(np.dot(np.transpose(eog_t), eog_t))  # performing pseudoinverse
    inv = np.dot(pseudoinv,np.transpose(eog_t))
    subtract_eog = np.dot(eog_t, np.dot(inv, eeg_t))
    clean_eeg = np.transpose(np.subtract(eeg_t, subtract_eog))  # subtracting the EOG noise from the EEG signal
    return clean_eeg;





