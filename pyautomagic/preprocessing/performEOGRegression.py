import numpy as np
import logging


def performEOGRegression(eeg, eog, *args):
    """
        Performs linear regression to remove EOG artifact from the EEG data

        :param eeg: EEG signal with the EOG artifacts
        :type eeg: np.ndarray
        :param eog: EOG signal
        :type eog: np.ndarray
        :param *args: variable length argument list
        :return: Cleaned EEG signal from EEG artifacts
        :rtype: np.ndarray
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
    inv = np.dot(pseudoinv,np.transpose(eog_t))
    subtract_eog = np.dot(eog_t, np.dot(inv, eeg_t))
    # subtracting the EOG noise from the EEG signal
    clean_eeg = np.transpose(np.subtract(eeg_t, subtract_eog))
    return clean_eeg




