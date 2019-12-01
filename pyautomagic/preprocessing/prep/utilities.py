import numpy as np
import logging
import math
from cmath import sqrt
import scipy.interpolate


def union(list1, list2):
    return list(set(list1 + list2))


def set_diff(list1, list2):
    return list(set(list1) - set(list2))


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


def filter_design(N_order, amp, freq, sample_rate):
    """Creates a FIR low-pass filter that filters the EEG data using frequency
    sampling method.

    Parameters
    __________
    N_order: int
             order of the filter
    amp: list of int
         amplitude vector for the frequencies
    freq: list of int
          frequency vector for which amplitude can be either 0 or 1
    sample_rate: int
          Sampling rate of the EEG signal
    Returns
    _______
    kernel: ndarray
            filter kernel

    """
    nfft = np.maximum(512, 2 ** (np.ceil(math.log(100) / math.log(2))))
    hamming_window = np.subtract(0.54, np.multiply(0.46, np.cos(
        np.divide(np.multiply(2 * math.pi, np.arange(N_order + 1)), N_order))))
    pchip_interpolate = scipy.interpolate.PchipInterpolator(np.round(np.multiply
                                                            (nfft, freq)), amp)
    freq = pchip_interpolate(np.arange(nfft + 1))
    freq = np.multiply(freq,
                       np.exp(np.divide(np.multiply(-(0.5 * N_order) * sqrt(-1) *
                        math.pi, np.arange(nfft + 1)), nfft)))
    kernel = np.real(np.fft.ifft(np.concatenate
                                 ([freq, np.conj(freq[len(freq) - 2:0:-1])])))
    kernel = np.multiply(kernel[0:N_order + 1],
                         (np.transpose(hamming_window[:])))
    return kernel
