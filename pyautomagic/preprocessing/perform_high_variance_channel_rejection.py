import logging
import numpy as np

logger = logging.getLogger(__name__)


def perform_high_variance_channel_rejection(
    data: np.ndarray, removed_mask: np.array, sd_threshold: float = 25
):
    """
    reject bad channels based on high standard deviation

    rejected = perform_high_variance_channel_rejection(data, removed_mask, sd_threshold)

    Here rejected is a list of channels that must be removed. data and removed_mask will be part of EEG_in structure.
    sd_threshold is an optional input for standard deviation threshold. When it is omitted, default value is used.

    :param data: data array of EEG
    :param removed_mask: mask of removed channels
    :param sd_threshold: threshold value for standard deviation
    :return: data_out : EEG data after channel rejection
    """

    # checking input arguments and if not acceptable, assigning default value.
    if not isinstance(sd_threshold, int) and not isinstance(sd_threshold, float):
        sd_threshold = 25
        logger.log("Invalid channel_criterion value. Default of 25 used.")

    # dimension of EEG data
    no_channels, _ = data.shape

    # initializing bad_channel_mask
    bad_channels_mask = np.zeros((1, no_channels), dtype=bool)

    # calculating standard deviation and rejecting channels with higher sd than threshold value
    rejected = np.nanstd(data, axis=1) > sd_threshold
    data[np.where(rejected)[0][0]] = 0
    data_out = data

    # updating other parameters of dataset accordingly
    bad_channels_mask[0][np.where(rejected)[0][0]] = True
    new_mask = np.copy(removed_mask)
    old_mask = np.copy(removed_mask)
    new_mask[np.where(new_mask == 0)[0]] = bad_channels_mask
    bad_channels = np.setdiff1d(np.where(new_mask), np.where(old_mask))
    removed_mask = new_mask

    return data_out, bad_channels, removed_mask
