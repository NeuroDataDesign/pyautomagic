import mne
import numpy as np
from utilities import set_diff, remove_reference
import noisy
from scipy.signal import detrend
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def robust_reference(EEG, reference_out, montage_kind='standard_1020'):
    """
    Detect bad channels by robust referencing
    This function implements the functionality of the `robustReference` function
    as part of the PREP pipeline for EEG data described in [1].

    Parameters
    ----------
    EEG : raw mne object
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
       EEG analysis. Frontiers in Neuroinformatics, 9, 16.
    """
    EEG.rename_channels(lambda s: s.strip("."))
    ch_names = EEG.info['ch_names']

    # Warn if evaluation and reference channels are not the same for robust
    if not set(reference_out.referenceChannels) == set(reference_out.evaluationChannels):
        logger.warning('robustReference: Reference channels and'
                       'evaluation channels should be same for robust reference')

    # Determine unusable channels and remove them from the reference channels
    EEG._data = detrend(EEG.get_data())

    signal_noisy = noisy.Noisydata(EEG)
    signal_noisy.find_all_bads()
    unusable_channels = list(set(signal_noisy.bad_by_nan + signal_noisy.bad_by_flat))
    reference_channels = set_diff(reference_out.referenceChannels, unusable_channels)

    # Get initial estimate of the mean by the specified method
    signal = EEG.get_data()
    ref_initial = np.median(EEG.get_data(picks=reference_channels), axis=0)
    unusable_index = [ch_names.index(ch) for ch in unusable_channels]
    signal_tmp = remove_reference(signal, ref_initial, unusable_index)

    # Remove reference from signal, iteratively interpolating bad channels
    EEG_tmp = EEG.copy()
    montage = mne.channels.read_montage(kind=montage_kind, ch_names=EEG_tmp.ch_names)
    EEG_tmp.set_montage(montage)

    iterations = 0
    noisy_channels_old = []
    max_iteration_num = 4
    while True:
        EEG_tmp._data = signal_tmp
        signal_noisy = noisy.Noisydata(EEG_tmp)
        signal_noisy.find_all_bads()
        noisy_channels = signal_noisy.get_bads(True)
        if iterations > 1 and (not noisy_channels or
                               set(noisy_channels) == set(noisy_channels_old)) or \
                iterations > max_iteration_num:
            break
        noisy_channels_old = noisy_channels.copy()

        if EEG_tmp.info['nchan']-len(noisy_channels) < 2:
            logger.error('robustReference:TooManyBad '
                         'Could not perform a robust reference -- not enough good channels')

        if noisy_channels:
            EEG_tmp._data = signal
            EEG_tmp.info['bads'] = noisy_channels
            EEG_tmp.interpolate_bads()
            signal_tmp = EEG_tmp.get_data()
        else:
            signal_tmp = signal
        reference_signal = np.nanmean(EEG_tmp.get_data(picks=reference_channels), axis=0)
        signal_tmp = remove_reference(signal, reference_signal, unusable_index)
        iterations = iterations + 1
        logger.info('Iterations: {}'.format(iterations))

    logger.info('Robust reference done')
    return noisy_channels
