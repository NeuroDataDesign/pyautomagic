import logging

import mne
import numpy as np


def performFilter(EEG, sfreq, filter_type=None, filt_freq=None, filter_length="auto"):
    """
    This function filters EEG data using Hamming windowed sinc FIR filter
    with input filter type and parameters.

    Parameters
    ----------
    EEG : ndarray, shape (…, n_times)
        Input EEG data to be filtered.
    sfreq : float | None
        The sample frequency in Hz.
    filter_type : str
        The filter type, can only take 'low', 'high' or 'notch', defaults to None
    filt_freq : float | None
        The filter frequency in Hz, defaults to None
    filter_length : str | int
        Length of the FIR filter to use, defaults to 'auto'.

    Returns
    -------
    ndarray, shape (…, n_times)
        The filtered EEG data.

    """
    if filter_type is None:
        logging.warning("No Filter Will be Performed")
        if filt_freq is not None:
            logging.warning("Unused filter parameter filt_freq")
        EEG_filt = EEG
    elif filter_type not in ("low", "high", "notch"):
        logging.error("filter_type must be 'low', 'high' or 'notch'")
    else:
        if filter_type == "low":
            if filt_freq is None:
                logging.warning(
                    "Upper pass-band freq is not given but is required. Default parameters"
                    "for low pass filtering will be used"
                )
                filt_freq = 30  # Default
            EEG_filt = mne.filter.filter_data(
                EEG,
                sfreq,
                None,
                filt_freq,
                picks=None,
                filter_length=filter_length,
                l_trans_bandwidth="auto",
                h_trans_bandwidth="auto",
                n_jobs=1,
                method="fir",
                phase="zero",
                fir_window="hamming",
                fir_design="firwin",
                pad="reflect_limited",
                verbose=None,
            )
        if filter_type == "high":
            if filt_freq is None:
                logging.warning(
                    "Lower pass-band freq is not given but is required. Default parameters"
                    "for high pass filtering will be used"
                )
                filt_freq = 0.5  # Default
            EEG_filt = mne.filter.filter_data(
                EEG,
                sfreq,
                filt_freq,
                None,
                picks=None,
                filter_length=filter_length,
                l_trans_bandwidth="auto",
                h_trans_bandwidth="auto",
                n_jobs=1,
                method="fir",
                phase="zero",
                fir_window="hamming",
                fir_design="firwin",
                pad="reflect_limited",
                verbose=None,
            )
        if filter_type == "notch":
            if filt_freq is None:
                logging.warning(
                    "Frequency for notch filter is not complete."
                    "The default will be used."
                )
                filt_freq = 60  # Default
            EEG_filt = mne.filter.notch_filter(
                EEG,
                sfreq,
                filt_freq,
                filter_length=filter_length,
                notch_widths=None,
                trans_bandwidth=1,
                method="fir",
                phase="zero",
                fir_window="hamming",
                fir_design="firwin",
                pad="reflect_limited",
                verbose=None,
            )
    return EEG_filt
