import logging

logger = logging.getLogger(__name__)

""""
 Rates datasets, based on quality measures calculated with calcQuality()
 Inputs: The structure quality_metrics with the following fields:

 OHA   - The ratio of data points that exceed the absolute value a certain
 CHV   - The ratio of channels in which % the standard deviation of the
         voltage amplitude
 THV   - The ratio of time points in which % the standard deviation of the
         voltage measures across all channels exceeds a certain threshold
         voltage measures across all time points exceeds a certain threshold
 MAV   - unthresholded mean absolute voltage of the dataset (not used in the current version)
 RBC   - ratio of bad channels

   The input is an EEG structure with optional parameters that can be
   passed within a structure: (e.g. struct('',50))
   
   'quality_metrics'        - a cell array indicating on which metrics the
                           datasets should be rated {'OHA','THV','CHV','RCB'}
   'overallGoodCutoff'      - cutoff for "Good" quality based on OHA [0.1]
   'overallBadCutoff'       - cutoff for "Bad" quality based on OHA [0.2]
   'timeGoodCutoff'         - cutoff for "Good" quality based on THV [0.1]
   'timeBadCutoff'          - cutoff for "Bad" quality based on THV [0.2]
   'channelGoodCutoff'      - cutoff for "Good" quality based on CHV [0.15]
   'channelBadCutoff'       - cutoff for "Bad" quality based on CHV [0.3]
   'badChannelGoodCutoff'   - cutoff for "Good" quality based on RBC[0.15]
   'badChannelBadCutoff'    - cutoff for "Bad" quality based on RBC[0.3]

"""


# Function that verifies thresholds between 0 and 1
def rateQuality(quality_metrics):
    if any(isinstance(x, int) for x in [quality_metrics]) or any(x <= 0 or x >= 1 for x in [quality_metrics]):
        logger.log(f"Some threshold cutoffs were set as integer. Please pass in a float between 0 and 1")
        raise ValueError("Incorrect value")


# Function classifies the dataset
def qualityRating(quality_metrics, overallGoodCutoff: float = 0.1, overallBadCutoff: float = 0.2,
                  timeGoodCutoff: float = 0.1, timeBadCutoff: float = 0.2,
                  channelGoodCutoff: float = 0.15, channelBadCutoff: float = 0.3, BadChannelGoodCutoff: float = 0.15,
                  BadChannelBadCutoff: float = 0.3):
    # Categorize wrt OHA
    if quality_metrics[0] < overallGoodCutoff:
        OHAq = 'Good'
    elif overallGoodCutoff <= quality_metrics[0] < overallBadCutoff:
        OHAq = 'Ok'
    else:
        OHAq = 'Bad'

    # Categorize wrt THV
    if quality_metrics[1] < timeGoodCutoff:
        THVq = 'Good'
    elif timeGoodCutoff <= quality_metrics[1] < timeBadCutoff:
        THVq = 'Ok'
    else:
        THVq = 'Bad'

    # Categorize wrt RBC
    if quality_metrics[2] < BadChannelGoodCutoff:
        RCBq = 'Good'
    elif BadChannelGoodCutoff <= quality_metrics[2] < BadChannelBadCutoff:
        RCBq = 'Ok'
    else:
        RCBq = 'Bad'

    # Categorize wrt CHV
    if quality_metrics[3] < channelGoodCutoff:
        CHVq = 'Good'
    elif channelGoodCutoff <= quality_metrics[3] < channelBadCutoff:
        CHVq = 'Ok'
    else:
        CHVq = 'Bad'

    # Combining ratings with the rule that the rating depends on the worst rating
    if any(OHAq or THVq or RCBq or CHVq) is 'Bad':
        rating = 'Bad Rating'

    elif any(OHAq or THVq or RCBq or CHVq) is 'Ok':
        rating = 'Ok Rating'

    else:
        rating = 'Good Rating'
        print(rating)

    # Print result
    return rating
