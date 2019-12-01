import mne
from scipy import signal


def prep_pipeline(raw, params):
    EEGData = raw.get_data()
    ch_names_original = raw.info["ch_names"]
    sample_rate = raw.info["sfreq"]
    mne.filter.filter_data(EEGData, sample_rate, 1, None, picks=None,
                           filter_length="auto", l_trans_bandwidth="auto",
                           h_trans_bandwidth="auto", n_jobs=1,
                           method="fir", iir_params=None,
                           copy=True, phase="zero", fir_window="hamming",
                           fir_design="firwin", pad="reflect_limited",
                           verbose=None)
    EEGData = signal.detrend(EEGData)

    # removing line noise
    linenoise = params.line_frequencies
    mne.filter.notch_filter(EEGData, sample_rate, linenoise, filter_length="auto",
                            notch_widths=None, trans_bandwidth=1, method="fir",
                            iir_params=None, mt_bandwidth=None,
                            p_value=0.05, picks=None, n_jobs=1, copy=True, phase="zero",
                            fir_window="hamming", ir_design="firwin", pad="reflect_limited",
                            verbose=None)
    # please get an mne raw output here

    # Detect bad channels with robust Referencing (I'll write this part)

    return bad_channels
