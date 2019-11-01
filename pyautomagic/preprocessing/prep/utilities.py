import numpy as np
import logging


def set_diff(list1, list2):
    return list(set(list1)-set(list2))


def remove_reference(signal, reference, exclude=None):
    """
    Remove the reference signal from the original EEG signal,
    with some unusable channels excluded.

    Parameters
    ----------
    signal : 2D array (channels * times)
        Original EEG signal
    reference : 1D array (length times)
        Reference signal
    exclude : list | None
        A list of unusable channel indexes to exclude when subtracting the reference

    Returns
    -------
    2D array (channels * times)
        The referenced EEG signal

    """
    if np.ndim(signal) != 2:
        logging.error('RemoveReference: EEG signal must be 2D array (channels * times)')
    signal_referenced = signal - reference
    if exclude:
        signal_referenced[exclude, :] = signal[exclude, :]
    return signal_referenced
