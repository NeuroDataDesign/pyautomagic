from typing import List
import logging
import numpy as np

logger = logging.getLogger(__name__)

class Quality():
    def calcQuality(self, Data: np.ndarray, bad_chans: List, overallThresh: float = 50, timeThresh: float = 25,
                    chanThresh: float = 25, apply_common_avg: bool = True):
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
        if not isinstance(overallThresh, int) and not isinstance(overallThresh, float):
            overallThresh = 50
            logger.log('Invalid overallThresh value. Default of 50 used.')
        if not isinstance(timeThresh, int) and not isinstance(timeThresh, float):
            timeThresh = 25
            logger.log('Invalid timeThresh value. Default of 25 used.')
        if not isinstance(chanThresh, int) and not isinstance(chanThresh, float):
            chanThresh = 25
            logger.log('Invalid chanThresh value. Default of 25 used.')
        if not isinstance(apply_common_avg, bool):
            # ADD STATEMENT TO ALLOW TYPICAL OTHER BOOLEAN INDICATORS
            apply_common_avg = True
            logger.log('Invalid apply_common_avg value. Average referencing used.')
        # ADD CHECKS FOR DAT AND BAD_CHANS?

        # get the dimensions of EEG data (# channels, # time points, # samples of data)
        n_chans, n_times, n_samples = Data.shape

        # perform average reference
        if apply_common_avg:
            avg_signal = np.mean(Data, axis=0)
            Data = Data - avg_signal

        # Calculating quality metrics
        # Overall high amplitude data points
        OHA = np.sum(np.absolute(Data) > overallThresh) / n_samples
        # Timepoints of high variance
        std_across_chans = np.std(Data, axis=0)
        THV = np.sum(std_across_chans > timeThresh) / n_times
        # Ratio of bad channels
        RBC = len(bad_chans) / float(n_chans)
        # Channels of high variance
        std_across_time = np.std(Data, axis=1)
        CHV = np.sum(std_across_time > chanThresh) / n_chans
        # unthresholded mean absolute voltage
        MAV = np.mean(np.absolute(Data))

        quality_metrics = {'OHA': OHA, 'THV': THV, 'RBC': RBC, 'CHV': CHV, 'MAV': MAV,  # actual results
                           'ot': overallThresh, 'tt': timeThresh, 'ct': chanThresh, # for development
                           'ar': apply_common_avg}  # for development
        return quality_metrics
