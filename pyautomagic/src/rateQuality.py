import logging

logger = logging.getLogger(__name__)

""""
 Rates datasets, based on quality measures calculated with calcQuality()
 
 Inputs: The dictionary quality_metrics{} with the following fields:

  overall_high_amp :   Overall high amplitude data points
  times_high_var   :   Time points of high variance across channels 
  ratio_bad_chans  :   Ratio of bad channels
  chan_high_var    :   Channels of high variance across time
  
 The input is an EEG structure with optional parameters that can be
 passed within a structure: 
   
   'quality_metrics'--------- a dictionary indicating on which metrics the
                              datasets should be rated
   'overallGoodCutoff'------- cutoff for "Good" quality based on 
                              overall high amplitude data points [0.1]
   'overallBadCutoff'-------- cutoff for "Bad" quality based on 
                              overall high amplitude data point [0.2]
   'timeGoodCutoff'---------- cutoff for "Good" quality based on 
                              time points of high variance across channels [0.1]
   'timeBadCutoff'----------- cutoff for "Bad" quality based on 
                              time points of high variance across channels [0.2]
   'badChannelGoodCutoff'---- cutoff for "Good" quality based on ratio of 
                              bad channels [0.15]
   'badChannelBadCutoff'----- cutoff for "Bad" quality based on ratio of 
                              bad channels [0.3]
   'channelGoodCutoff'------- cutoff for "Good" quality based on channels 
                              of high variance across time [0.15]
   'channelBadCutoff'-------- cutoff for "Bad" quality based on channels 
                              of high variance across time [0.3]

 The output is a dictionary indicating if the dataset is "Good" = 100, "Regular" = 50 or "Bad" = 0 

"""


# Function that rates EEG datasets depending on quality_metrics values and predefined rating values
def rateQuality(quality_metrics, overallGoodCutoff: float = 0.1, overallBadCutoff: float = 0.2,
                timeGoodCutoff: float = 0.1, timeBadCutoff: float = 0.2,
                badChannelGoodCutoff: float = 0.15, badChannelBadCutoff: float = 0.3, channelGoodCutoff: float = 0.15,
                channelBadCutoff: float = 0.3):

    # Check that the values in quality_metrics{} are positive numbers not equal to 0
    if not isinstance(quality_metrics.values(), int) and not isinstance(quality_metrics.values(), float) or isinstance(quality_metrics.values(), bool) or (quality_metrics.values() <= 0):
        logger.error("Some value of Quality Metrics is not a number, please verify your EEG input data")

    # Rating of EEG DATA according to the values of quality_metrics
    if quality_metrics['overall_high_amp'] > overallBadCutoff or quality_metrics['times_high_var'] > timeBadCutoff or quality_metrics['ratio_bad_chans'] > badChannelBadCutoff or quality_metrics['chan_high_var'] > channelBadCutoff:
        dataset_qualification = {'dataset_qualification': 0}  # Bad EEG dataset rating
        return dataset_qualification
    elif quality_metrics['overall_high_amp'] < overallGoodCutoff and quality_metrics['times_high_var'] < timeGoodCutoff and quality_metrics['ratio_bad_chans'] < badChannelGoodCutoff and quality_metrics['chan_high_var'] < channelGoodCutoff:
        dataset_qualification = {'dataset_qualification': 100}  # Good EEG dataset rating
        return dataset_qualification
    else:
        dataset_qualification = {'dataset_qualification': 50}  # Regular EEG dataset rating
        return dataset_qualification
