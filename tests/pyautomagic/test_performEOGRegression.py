import logging

import numpy as np
import pytest


def performEOGRegression(eeg, eog, *args):
    """Performs linear regression to remove EOG artifact from the EEG data

    Parameters
    ----------
    eeg: np.ndarray
        EEG signal with the EOG artifacts
    eog: np.ndarray
        EOG signal
    *args
        variable length argument list

    Returns
    -------
    clean_eeg: np.ndarray
               Cleaned EEG signal from EEG artifacts

    """
    # checks if EOG Regression should be skipped or not depending on the function arguments
    if len(args[0]) == 0:
        logging.warning('EOG regression skipped')
        return

    size_eeg = np.shape(eeg)
    size_eog = np.shape(eog)
    dimension = len(size_eog)
    # resizing the EOG array so that its pseudoinverse can be calculated
    if dimension == 1:
        eog.resize((1, size_eog[0]))
    eeg_t = np.transpose(eeg)
    eog_t = np.transpose(eog)
    # performing pseudoinverse
    pseudoinv = np.linalg.pinv(np.dot(np.transpose(eog_t), eog_t))
    inv = np.dot(pseudoinv, np.transpose(eog_t))
    subtract_eog = np.dot(eog_t, np.dot(inv, eeg_t))
    # subtracting the EOG noise from the EEG signal
    clean_eeg = np.transpose(np.subtract(eeg_t, subtract_eog))
    return clean_eeg


def test_performEOGRegression():
    eeg=np.array([[1, 2, 4, 0.8], [0.1, 0.2, 0.4, 0.9]])
    eog=np.array([[9, 10, 11, 12], [10, 12, 3, 4]])
    assert np.array_equal(np.round(performEOGRegression(eeg, eog, {"PerformEOGRegression": "Yes"}), 2), np.round(np.array([[-0.42197603, 0.47275097, 1.71501431, -1.64957357], [-0.07695577, 0.04392939, -0.2369535, 0.23831638]]),2))

