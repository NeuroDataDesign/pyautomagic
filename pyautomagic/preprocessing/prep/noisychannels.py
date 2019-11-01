import numpy as np
from scipy.io import loadmat
from statsmodels import robust
import mne
from scipy import signal
from scipy.stats import iqr
import scipy.interpolate
import math
from cmath import sqrt
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from mne.channels.interpolation import _make_interpolation_matrix


def find_noisy_channels(raw, linenoise):
    """ High-pass filters, detrends, and removes line noise from the EEG data. Additionally
     finds channels having Nans, no data, unusually high amplitudes poor correlation,
     high-frequency noise, and bad correlation in the low frequency portion of the signal
     using RANSAC.

     Inspired by the PREP pipleine [1]. Fischler and Bolles RANSAC method was used for
     finding outlier channels [2].

     Parameters
     __________
     raw:  raw mne object
           contains the EEG data and other information related to it
     linenoise: int
                line frequency that needs to be removed by notch filtering
     Raises
     ______
     IOE error
            If too few channels are present to perfom RANSAC

     Returns
     _______
     noisy_channels: list of string
                     list of the names of all the bad channels
     References
     __________

     [1] Bigdely-Shamlo, N., Mullen, T., Kothe, C., Su, K., & Robbins, K. (2015).
     The PREP pipeline: standardized preprocessing for large-scale EEG analysis.
     Frontiers In Neuroinformatics, 9. doi: 10.3389/fninf.2015.00016
     [2] Fischler, M., & Bolles, R. (1981). Random sample consensus: a paradigm
     for model fitting with applications to image analysis and automated
     cartography. Communications Of The ACM, 24(6), 381-395. doi: 10.1145/358669.358692

     """
    EEGData = raw.get_data()
    ch_names_original = raw.info["ch_names"]
    sample_rate = raw.info["sfreq"]
    mne.filter.filter_data(EEGData,sample_rate, 1, None, picks=None,
                           filter_length="auto", l_trans_bandwidth="auto",
                           h_trans_bandwidth="auto", n_jobs=1,
                           method="fir", iir_params=None,
                           copy=True,phase="zero",fir_window="hamming",
                           fir_design="firwin",pad="reflect_limited",
                           verbose=None)
    EEGData = signal.detrend(EEGData)
    # removing line noise
    mne.filter.notch_filter(EEGData,sample_rate,linenoise,filter_length="auto",
                            notch_widths=None,trans_bandwidth=1,method="fir",
                            iir_params=None,mt_bandwidth=None,
                            p_value=0.05,picks=None,n_jobs=1,copy=True,phase="zero",
                            fir_window="hamming",ir_design="firwin",pad="reflect_limited",
                            verbose=None)
    # finding channels with NaNs or constant values for long periods of time
    original_dimensions = np.shape(EEGData)
    original_channels = np.arange(original_dimensions[0])
    channels_interpolate = original_channels
    nan_channel_mask = [False] * original_dimensions[0]
    no_signal_channel_mask = [False] * original_dimensions[0]

    for i in range(0, original_dimensions[0]):
        nan_channel_mask[i] = np.sum(np.isnan(EEGData[i, :])) > 0
    for i in range(0, original_dimensions[0]):
        no_signal_channel_mask[i] = robust.mad(EEGData[i, :]) < 10 ** (-10) or np.std(
            EEGData[i, :]) < 10 ** (-10)
    nan_channels = channels_interpolate[nan_channel_mask]
    no_data_channels = channels_interpolate[no_signal_channel_mask]
    for i in range(0, original_dimensions[0]):
        if nan_channel_mask[i] == True or no_signal_channel_mask[i] == True:
            EEGData = np.delete(EEGData, i, axis=0)
    nans_no_data_channels = np.union1d(nan_channels, no_data_channels)
    channels_interpolate = np.setdiff1d(
    channels_interpolate, nans_no_data_channels)
    nans_no_data_ChannelName = list()
    ch_names = raw.info["ch_names"]
    for i in range(0, len(nans_no_data_channels)):
        nans_no_data_ChannelName.append(ch_names[nans_no_data_channels[i]])
    raw.drop_channels(nans_no_data_ChannelName)
    evaluation_channels = channels_interpolate
    new_dimension = np.shape(EEGData)

    # find channels that have abnormally high or low amplitude
    robust_channel_deviation = np.zeros(original_dimensions[0])
    deviation_channel_mask = [False] * (new_dimension[0])
    channel_deviation = np.zeros(new_dimension[0])
    for i in range(0, new_dimension[0]):
        channel_deviation[i] = 0.7413 * iqr(EEGData[i, :])
    channel_deviationSD = 0.7413 * iqr(channel_deviation)
    channel_deviationMedian = np.nanmedian(channel_deviation)
    robust_channel_deviation[evaluation_channels] = np.divide(
        np.subtract(channel_deviation, channel_deviationMedian), channel_deviationSD
    )
    for i in range(0, new_dimension[0]):
        deviation_channel_mask[i] = abs(robust_channel_deviation[i]) > 5 or np.isnan(
            robust_channel_deviation[i]
        )
    deviation_channels = evaluation_channels[deviation_channel_mask]
    # finding channels with high frequency noise
    EEGData = np.transpose(EEGData)
    dimension = np.shape(EEGData)
    if sample_rate > 100:
        new_EEG = np.zeros((dimension[0], dimension[1]))
        bandpass_filter = filter_design(
            N_order=100,
            amp=np.array([1, 1, 0, 0]),
            freq=np.array([0, 0.36, 0.4, 1]),
            sample_rate=sample_rate)
        for i in range(0, dimension[1]):
            new_EEG[:, i] = signal.filtfilt(bandpass_filter, 1, EEGData[:, i])
        noisiness = np.divide(robust.mad(np.subtract(EEGData, new_EEG)),
                              robust.mad(new_EEG))
        noisiness_median = np.nanmedian(noisiness)
        noiseSD = (np.median(np.absolute(np.subtract(noisiness, np.median(noisiness))))
                   * 1.4826)
        zscore_HFNoise = np.divide(np.subtract(noisiness, noisiness_median), noiseSD)
        HFnoise_channel_mask = [False] * new_dimension[0]
        for i in range(0, new_dimension[0]):
            HFnoise_channel_mask[i] = zscore_HFNoise[i] > 5 or np.isnan(
                zscore_HFNoise[i])
    else:
        new_EEG = EEGData
        noisiness_median = 0
        noisinessSD = 1
        zscore_HFNoise = np.zeros(dimension[1], 1)
        HFNoise_channels = []
    HFNoise_channels = evaluation_channels[HFnoise_channel_mask]
    # finding channels by correlation
    CORRELATION_SECONDS = 1  # default value
    CORRELATION_FRAMES = CORRELATION_SECONDS * sample_rate
    correlation_window = np.arange(CORRELATION_FRAMES)
    correlation_offsets = np.arange(1, dimension[0] - CORRELATION_FRAMES,
                                    CORRELATION_FRAMES)
    w_correlation = len(correlation_offsets)
    maximum_correlations = np.ones((original_dimensions[0], w_correlation))
    drop_out = np.zeros((dimension[1], w_correlation))
    channel_correlation = np.ones((w_correlation, dimension[1]))
    noiselevels = np.zeros((w_correlation, dimension[1]))
    channel_deviations = np.zeros((w_correlation, dimension[1]))
    drop = np.zeros((w_correlation, dimension[1]))
    len_correlation_window = len(correlation_window)
    EEG_new_win = np.reshape(
        np.transpose(new_EEG[0: len_correlation_window * w_correlation, :]),
        (dimension[1], len_correlation_window, w_correlation),
        order="F")
    data_win = np.reshape(
        np.transpose(EEGData[0: len_correlation_window * w_correlation, :]),
        (dimension[1], len_correlation_window, w_correlation),
        order="F")
    for k in range(0, w_correlation):
        eeg_portion = np.transpose(np.squeeze(EEG_new_win[:, :, k]))
        data_portion = np.transpose(np.squeeze(data_win[:, :, k]))
        window_correlation = np.corrcoef(np.transpose(eeg_portion))
        abs_corr = np.abs(
            np.subtract(window_correlation, np.diag(np.diag(window_correlation))))
        channel_correlation[k, :] = np.quantile(
            abs_corr, 0.98, axis=0)  # problem is here is solved
        noiselevels[k, :] = np.divide(
            robust.mad(np.subtract(data_portion, eeg_portion)), robust.mad(eeg_portion))
        channel_deviations[k, :] = 0.7413 * iqr(data_portion, axis=0)
    for i in range(0, w_correlation):
        for j in range(0, dimension[1]):
            drop[i, j] = np.int(
                np.isnan(channel_correlation[i, j]) or np.isnan(noiselevels[i, j]))
            if drop[i, j] == 1:
                channel_deviations[i, j] = 0
                noiselevels[i, j] = 0
    maximum_correlations[evaluation_channels, :] = np.transpose(channel_correlation)
    drop_out[:] = np.transpose(drop)
    noiselevels_out = np.transpose(noiselevels)
    channel_deviations_out = np.transpose(channel_deviations)
    thresholded_correlations = maximum_correlations < 0.4
    thresholded_correlations = thresholded_correlations.astype(int)
    fraction_BadCorrelationWindows = np.mean(thresholded_correlations, axis=1)
    fraction_BadDropOutWindows = np.mean(drop_out, axis=1)

    badCorrelation_channels = np.where(fraction_BadCorrelationWindows > 0.01)
    badCorrelation_channels_out = badCorrelation_channels[:]
    dropout_channels = np.where(fraction_BadDropOutWindows > 0.01)
    dropout_channels_out = dropout_channels[:]
    # medianMaxCorrelation = np.median(maximumCorrelations, 2);

    badSNR_channels = np.union1d(badCorrelation_channels_out, HFNoise_channels)
    noisy_channels = np.union1d(np.union1d(np.union1d(deviation_channels,
                    np.union1d(badCorrelation_channels_out, dropout_channels_out)),
                     badSNR_channels), np.union1d(nan_channels, no_data_channels))

    # performing ransac
    bads = list()
    for i in range(0, len(noisy_channels)):
        bads.append(ch_names[noisy_channels[i]])
    SAMPLES = 50
    FRACTION_GOOD = 0.25
    CORR_THRESH = 0.75
    FRACTION_BAD = (0.4,)
    CORR_WIN_SEC = 4
    chn_pos = raw._get_channel_positions()
    raw.info["bads"] = bads
    good_chn_labs = list()
    good_idx = mne.pick_channels(ch_names, include=[], exclude=raw.info["bads"])
    for i in range(0, len(good_idx)):
        good_chn_labs.append(ch_names[good_idx[i]])
    n_chans_good = good_idx.shape[0]
    chn_pos_good = chn_pos[good_idx, :]
    n_pred_chns = int(np.ceil(FRACTION_GOOD * n_chans_good))
    EEGData_filtered = np.transpose(new_EEG)
    if n_pred_chns <= 3:
        raise IOError("Too few channels available to reliably perform ransac.")

    # Make the ransac predictions
    ransac_eeg = run_ransac(chn_pos=chn_pos, chn_pos_good=chn_pos_good,
        good_chn_labs=good_chn_labs, n_pred_chns=n_pred_chns,
        data=EEGData_filtered, n_samples=SAMPLES, raw=raw)
    signal_len = original_dimensions[1]
    n_chans = len(chn_pos)
    correlation_frames = CORR_WIN_SEC * raw.info["sfreq"]
    correlation_window = np.arange(correlation_frames)
    n = correlation_window.shape[0]
    correlation_offsets = np.arange(
        0, (signal_len - correlation_frames), correlation_frames)
    w_correlation = correlation_offsets.shape[0]
    data_window = EEGData_filtered[:n_chans, : n * w_correlation]
    data_window = data_window.reshape(n_chans, n, w_correlation)
    pred_window = ransac_eeg[:n_chans, : n * w_correlation]
    pred_window = pred_window.reshape(n_chans, n, w_correlation)
    channel_correlations = np.ones((w_correlation, n_chans))
    for k in range(w_correlation):
        data_portion = data_window[:, :, k]
        pred_portion = pred_window[:, :, k]
        corr = np.corrcoef(data_portion, pred_portion)
        corr = np.diag(corr[0:n_chans, n_chans:])
        channel_correlations[k, :] = corr

    thresholded_correlations = channel_correlations < CORR_THRESH
    frac_bad_corr_windows = np.mean(thresholded_correlations, axis=0)
    # find the corresponding channel names and return
    bad_idxs_bool = frac_bad_corr_windows > FRACTION_BAD
    bad_idxs = np.argwhere(bad_idxs_bool)
    bad_by_ransac = list()
    noisy_channels = np.union1d(noisy_channels, bad_idxs[0: len(bad_idxs)][0])
    ransac_channel_correlations = channel_correlations
    noisy_channels_list = list()
    for i in range(0, len(noisy_channels)):
        noisy_channels_list.append(ch_names_original[noisy_channels[i]])
    print(noisy_channels_list)
    return noisy_channels_list

def run_ransac(chn_pos, chn_pos_good, good_chn_labs, n_pred_chns, data, n_samples, raw):
    """Detects noisy channels apart from the ones described previously. It creates
    a random subset of the so-far good channels
    and predicts the values of the channels not in the subset.

    Parameters
    __________
    chn_pos: ndarray
             3-D coordinates of the electrode position
    chn_pos_good: ndarray
                  3-D coordinates of all the channels not detected noisy so far
    good_chn_labs: array_like
                    channel labels for the ch_pos_good channels-
    n_pred_chns: int
                 channel numbers used for interpolation for RANSAC
    data: ndarry
          2-D EEG data
    n_samples: int
                number of interpolations from which a median will be computed
    raw: raw mne object
         contains the EEG data and information associated with it
    Returns
    _______
    ransac_eeg: ndarray
                The EEG data predicted by RANSAC

    Title: noisy
    Author: Stefan Appelhoff
    Date: 2018
    Availability: https://github.com/sappelhoff/pyprep/blob/master/pyprep/noisy.py

    """
    n_chns, n_timepts = np.shape(data)
    eeg_predictions = np.zeros((n_chns, n_timepts, n_samples))
    for sample in range(n_samples):
        eeg_predictions[..., sample] = get_ransac_pred(
            chn_pos, chn_pos_good, good_chn_labs, n_pred_chns, raw, data
        )

    ransac_eeg = np.median(eeg_predictions, axis=-1, overwrite_input=True)
    return ransac_eeg


def get_ransac_pred(chn_pos, chn_pos_good, good_chn_labs, n_pred_chns, raw, data):
    """Performs RANSAC prediction

        Parameters
        __________
        chn_pos: ndarray
                 3-D coordinates of the electrode position
        chn_pos_good: ndarray
                      3-D coordinates of all the channels not detected noisy so far
        good_chn_labs: array_like
                        channel labels for the ch_pos_good channels
        n_pred_chns: int
                     channel numbers used for interpolation for RANSAC
        data: ndarry
              2-D EEG data
        raw: raw mne object
             contains the EEG data and information associated with it
        Returns
        _______
        ransac_pred: ndarray
                    Single RANSAC prediction

        Title: noisy
        Author: Stefan Appelhoff
        Date: 2018
        Availability: https://github.com/sappelhoff/pyprep/blob/master/pyprep/noisy.py

"""
    ch_names = raw.info["ch_names"]
    reconstr_idx = np.random.choice(
        np.arange(chn_pos_good.shape[0]), size=n_pred_chns, replace=False)
    reconstr_labels = list()
    reconstr_pos = np.zeros((len(reconstr_idx), 3))
    for i in range(0, len(reconstr_idx)):
        reconstr_labels.append(good_chn_labs[reconstr_idx[i]])
        reconstr_pos[i, :] = chn_pos_good[reconstr_idx[i], :]

    reconstr_picks = [list(ch_names).index(chn_lab) for chn_lab in reconstr_labels]
    interpol_mat = _make_interpolation_matrix(reconstr_pos, chn_pos)
    ransac_pred = np.matmul(interpol_mat, data[reconstr_picks, :])
    return ransac_pred


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


raw = mne.io.read_raw_edf("C:\\Users\\Aamna\\Desktop\\NDD\\S001R01.edf", preload=True)
raw.rename_channels(lambda s: s.strip("."))
montage = mne.channels.read_montage(
    kind="standard_1020", ch_names=raw.info["ch_names"]
)
mne.set_log_level("WARNING")
raw.set_montage(montage)
bads = find_noisy_channels(raw, linenoise=50)
raw.info["bads"] = bads
raw.interpolate_bads(reset_bads="False")
