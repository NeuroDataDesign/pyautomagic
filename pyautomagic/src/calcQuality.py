import logging
from typing import List

import numpy as np

logger = logging.getLogger(__name__)


def calcQuality(
    data: np.ndarray,
    bad_chans: List,
    overallThresh: float = 50,
    timeThresh: float = 25,
    chanThresh: float = 25,
    apply_common_avg: bool = True,
):
    """
    Calculates four essential quality metrics of a data set and returns a dictionary of the quality metrics and thresholds/settings used

    The four quality metrics:
        Overall high amplitude data points
        Timepoints of high variance across channels
        Ratio of bad channels
        Channels of high variance across time

    Mean absolute voltage is also calculated.

    :param Data: a channels x timepoints data array of EEG
    :type Data: np.ndarray
    :param bad_chans:  a list of the numbers of bad channels
    :type bad_chans: list
    :param overallThresh: overall threshold for rejection of ...
    :type overallThresh: float
    :param timeThresh: threshold for rejecting time segments
    :type timeThresh: float
    :param chanThresh: threshold for rejecting channels
    :type chanThresh: float
    :param apply_common_avg: if average referencing should be applied
    :type apply_common_avg: bool
    :return: quality_metrics: a dictionary of the quality metrics and thresholds/settings used
        The four quality metrics:
        Overall high amplitude data points
        Timepoints of high variance across channels
        Ratio of bad channels
        Channels of high variance across time

        Mean absolute voltage also calculated
    :rtype: dict
    """
    # checking all of the default value types, if not what they should be, use default
    if (
        not isinstance(overallThresh, int)
        and not isinstance(overallThresh, float)
        or isinstance(overallThresh, bool)
        or (overallThresh <= 0)
    ):
        overallThresh = 50
        logger.log(30, "Invalid overallThresh value. Default of 50 used.")
    if (
        not isinstance(timeThresh, int)
        and not isinstance(timeThresh, float)
        or isinstance(timeThresh, bool)
        or (timeThresh <= 0)
    ):
        timeThresh = 25
        logger.log(30, "Invalid timeThresh value. Default of 25 used.")
    if (
        not isinstance(chanThresh, int)
        and not isinstance(chanThresh, float)
        or isinstance(chanThresh, bool)
        or (chanThresh <= 0)
    ):
        chanThresh = 25
        logger.log(30, "Invalid chanThresh value. Default of 25 used.")
    if not isinstance(apply_common_avg, bool):
        # ADD STATEMENT TO ALLOW TYPICAL OTHER BOOLEAN INDICATORS
        apply_common_avg = True
        logger.log(30, "Invalid apply_common_avg value. Average referencing used.")
    # ADD CHECKS FOR DAT AND BAD_CHANS?

    # get the dimensions of EEG data (# channels, # time points, # samples of data)
    n_chans, n_times = data.shape
    n_samples = n_chans * n_times
    # perform average reference
    if apply_common_avg:
        avg_signal = np.mean(data, axis=0)
        data = data - avg_signal

    # Calculating quality metrics
    # Overall high amplitude data points
    overall_high_amp = np.sum(np.absolute(data) > overallThresh) / n_samples
    # Timepoints of high variance
    std_across_chans = np.sqrt(
        (np.sum(abs(data - np.mean(data, 0)) ** 2, 0)) / (n_chans - 1)
    )  # matching matlab std def
    times_high_var = np.sum(std_across_chans > timeThresh) / n_times
    # Ratio of bad channels
    ratio_bad_chans = len(bad_chans) / float(n_chans)
    # Channels of high variance
    std_across_time = np.std(data, axis=1)
    chan_high_var = np.sum(std_across_time > chanThresh) / n_chans
    # unthresholded mean absolute voltage
    mean_abs_volt = np.mean(np.absolute(data))

    quality_metrics = {
        "overall_high_amp": overall_high_amp,
        "times_high_var": times_high_var,
        "ratio_bad_chans": ratio_bad_chans,
        "chan_high_var": chan_high_var,
        "mean_abs_volt": mean_abs_volt,
    }  # for development
    return quality_metrics
