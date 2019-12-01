import mne
import numpy as np
from utilities import union, set_diff, remove_reference
import noisy
from noisychannels import bad_channels_detector
from scipy.signal import detrend
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def robust_reference(raw, reference_out, montage_kind='standard_1020'):
    """
    Detect bad channels by robust referencing
    This function implements the functionality of the `robustReference` function
    as part of the PREP pipeline for raw data described in [1].

    Parameters
    ----------
    raw : raw mne object
    reference_out : Reference structure with at least the following parameters:
        referenceChannels
        evaluationChannels
    montage_kind : str
        Which kind of montage should be used to infer the electrode
        positions? E.g., 'standard_1020'

    Returns
    -------
    list
        A list of names of noisy channels

    References
    ----------
    .. [1] Bigdely-Shamlo, N., Mullen, T., Kothe, C., Su, K. M., Robbins, K. A.
       (2015). The PREP pipeline: standardized preprocessing for large-scale
       raw analysis. Frontiers in Neuroinformatics, 9, 16.
    """
    raw.rename_channels(lambda s: s.strip("."))
    ch_names = raw.info['ch_names']

    # Warn if evaluation and reference channels are not the same for robust
    if not set(reference_out['ref_chs']) == set(reference_out['eval_chs']):
        logger.warning('robustReference: Reference channels and'
                       'evaluation channels should be same for robust reference')

    # raw._data = detrend(raw.get_data())

    # Determine unusable channels and remove them from the reference channels
    signal_noisy = bad_channels_detector(raw)
    signal_noisy.find_noisy_channels()
    noisy_channels = {'bad_by_nan': signal_noisy.bad_by_nan,
                      'bad_by_flat': signal_noisy.bad_by_flat,
                      'bad_by_deviation': signal_noisy.bad_by_deviation,
                      'bad_by_hf_noise': signal_noisy.bad_by_hf_noise,
                      'bad_by_correlation': signal_noisy.bad_by_correlation,
                      'bad_by_dropout': signal_noisy.bad_by_dropout,
                      'bad_by_ransac': signal_noisy.bad_by_ransac,
                      'bad_all': signal_noisy.get_bads()}
    logger.info('Bad channels: {}'.format(noisy_channels))

    unusable_channels = list(set(signal_noisy.bad_by_nan + signal_noisy.bad_by_flat))
    reference_channels = set_diff(reference_out['ref_chs'], unusable_channels)

    # Get initial estimate of the mean by the specified method
    signal = raw.get_data()
    ref_initial = np.median(raw.get_data(picks=reference_channels), axis=0)
    unusable_index = [ch_names.index(ch) for ch in unusable_channels]
    signal_tmp = remove_reference(signal, ref_initial, unusable_index)

    # Remove reference from signal, iteratively interpolating bad channels
    raw_tmp = raw.copy()
    montage = mne.channels.read_montage(kind=montage_kind, ch_names=raw_tmp.ch_names)
    raw_tmp.set_montage(montage)

    iterations = 0
    noisy_channels_old = []
    max_iteration_num = 4

    while True:
        raw_tmp._data = signal_tmp
        signal_noisy = bad_channels_detector(raw_tmp)
        signal_noisy.find_noisy_channels()
        noisy_channels['bad_by_nan'] = union(noisy_channels['bad_by_nan'], signal_noisy.bad_by_nan)
        noisy_channels['bad_by_flat'] = union(noisy_channels['bad_by_flat'], signal_noisy.bad_by_flat)
        noisy_channels['bad_by_deviation'] = union(noisy_channels['bad_by_deviation'], signal_noisy.bad_by_deviation)
        noisy_channels['bad_by_hf_noise'] = union(noisy_channels['bad_by_hf_noise'], signal_noisy.bad_by_hf_noise)
        noisy_channels['bad_by_correlation'] = union(noisy_channels['bad_by_correlation'],
                                                     signal_noisy.bad_by_correlation)
        noisy_channels['bad_by_dropout'] = union(noisy_channels['bad_by_dropout'], signal_noisy.bad_by_dropout)
        noisy_channels['bad_by_ransac'] = union(noisy_channels['bad_by_ransac'], signal_noisy.bad_by_ransac)
        noisy_channels['bad_all'] = union(noisy_channels['bad_all'], signal_noisy.get_bads())
        logger.info('Bad channels: {}'.format(noisy_channels))

        if iterations > 1 and (not noisy_channels['bad_all'] or
                               set(noisy_channels['bad_all']) == set(noisy_channels_old)) or \
                iterations > max_iteration_num:
            break
        noisy_channels_old = noisy_channels['bad_all'].copy()

        if raw_tmp.info['nchan']-len(noisy_channels['bad_all']) < 2:
            logger.error('robustReference:TooManyBad '
                         'Could not perform a robust reference -- not enough good channels')

        if noisy_channels['bad_all']:
            raw_tmp._data = signal
            raw_tmp.info['bads'] = noisy_channels['bad_all']
            raw_tmp.interpolate_bads()
            signal_tmp = raw_tmp.get_data()
        else:
            signal_tmp = signal
        reference_signal = np.nanmean(raw_tmp.get_data(picks=reference_channels), axis=0)
        signal_tmp = remove_reference(signal, reference_signal, unusable_index)
        iterations = iterations + 1
        logger.info('Iterations: {}'.format(iterations))

    logger.info('Robust reference done')
    return noisy_channels
