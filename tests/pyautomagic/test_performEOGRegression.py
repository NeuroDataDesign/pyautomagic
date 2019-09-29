import pytest
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
        eog.resize((1, size_eog[0]))

    # performing linear regression
    eeg_t = np.transpose(eeg)
    eog_t = np.transpose(eog)

    pseudoinv = np.linalg.pinv(np.dot(np.transpose(eog_t), eog_t))
    inv = np.dot(pseudoinv, np.transpose(eog_t))
    subtract_eog = np.dot(eog_t, np.dot(inv, eeg_t))
    cleanEEG = np.transpose(np.subtract(eeg_t, subtract_eog))
    return cleanEEG


def test_performEOGRegression():
    eeg=np.array([[1, 2, 4, 0.8], [0.1, 0.2, 0.4, 0.9]])
    eog=np.array([[9, 10, 11, 12], [10, 12, 3, 4]])
    assert np.array_equal(np.round(performEOGRegression(eeg, eog), 2), np.round(np.array([[-0.42197603, 0.47275097, 1.71501431, -1.64957357], [-0.07695577, 0.04392939, -0.2369535, 0.23831638]]),2))

