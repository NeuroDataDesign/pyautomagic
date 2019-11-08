import numpy as np
import logging
import mne


def performEOGRegression(raw):
    """Performs linear regression to remove EOG artifact from the EEG data

        Parameters
        ----------
        raw: MNE raw data structure

        Returns
        -------
        clean_EEG: np.ndarray
                   Cleaned EEG signal from EOG artifacts

        """

    EEG=raw.get_data()
    EOG_idx=mne.pick_types(raw.info, eog=True)
    EOG=EEG[EOG_idx]
    # checks if EOG Regression should be skipped or not depending on whether EOG was recorded
    if EOG_idx.shape[0] == 0:
        logging.warning('EOG regression skipped')
        return

    size_EOG = EOG.shape
    dim = len(size_EOG)
    # resizing the EOG array so that its pseudoinverse can be calculated
    if dim == 1:
        EOG.resize((1, size_EOG[0]))
    EEG_t = np.transpose(EEG)
    EOG_t = np.transpose(EOG)
    # performing pseudoinverse
    pseudoinv = np.linalg.pinv(np.dot(np.transpose(EOG_t), EOG_t))
    inv = np.dot(pseudoinv,np.transpose(EOG_t))
    subtract_EOG = np.dot(EOG_t, np.dot(inv, EEG_t))
    # subtracting the EOG noise from the EEG signal
    clean_EEG = np.transpose(np.subtract(EEG_t, subtract_EOG))
    return clean_EEG



