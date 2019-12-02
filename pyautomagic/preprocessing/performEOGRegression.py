import numpy as np


def perform_EOG_regression(EEG, EOG):
    """The artifacts due to EOG activity are removed from the EEG data using the subtraction method
        that relies on the linear transformation of the EEG signal

        Parameters
        ----------
        EEG: np.ndarray
             The input EEG data
        EOG: np.ndarray
             The input EOG data

        Returns
        -------
        clean_EEG: np.ndarray
                   Cleaned EEG signal from EOG artifacts

        References
        __________
        [1] Pedroni, A., Bahreini, A., & Langer, N. (2019). Automagic: Standardized preprocessing of big EEG data.
        Neuroimage, 200, 460-473. doi: 10.1016/j.neuroimage.2019.06.046
        """

    size_EEG = np.shape(EEG)
    size_EOG = np.shape(EOG)
    dimension1 = len(size_EOG)
    dimension2 = len(size_EEG)
    # resizing the EOG array so that its pseudoinverse can be calculated
    if dimension1 == 1:
        EOG.resize((1, size_EOG[0]))
    if dimension2 == 1:
        EEG.resize((1, size_EEG[0]))

    EEG_t = np.transpose(EEG)
    EOG_t = np.transpose(EOG)
    # performing pseudoinverse
    pseudoinv = np.linalg.pinv(np.dot(np.transpose(EOG_t), EOG_t))
    inv = np.dot(pseudoinv, np.transpose(EOG_t))
    subtract_EOG = np.dot(EOG_t, np.dot(inv, EEG_t))
    # subtracting the EOG noise from the EEG signal
    clean_EEG = np.transpose(np.subtract(EEG_t, subtract_EOG))
    return clean_EEG
