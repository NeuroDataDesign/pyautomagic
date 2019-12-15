# Copyright 2019 NeuroData (http://neurodata.io)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import pprint

logger = logging.getLogger(__name__)


# Function that rates EEG datasets depending on quality_metrics values and predefined rating values
def rateQuality(
    quality_metrics,
    overall_Good_Cutoff: float = 0.1,
    overall_Bad_Cutoff: float = 0.2,
    time_Good_Cutoff: float = 0.1,
    time_Bad_Cutoff: float = 0.2,
    bad_Channel_Good_Cutoff: float = 0.15,
    bad_Channel_Bad_Cutoff: float = 0.3,
    channel_Good_Cutoff: float = 0.15,
    channel_Bad_Cutoff: float = 0.3,
):
    """
    Rates datasets, based on quality measures calculated with calcQuality().

    The possible ratings:
        Good overall rating
        Regular overall rating
        Bad overall rating

    Parameters
    ----------
    quality_metrics : dict
                    a dictionary containing the quality metrics to rate the dataset.

    overall_Good_Cutoff : float
                    cutoff for "Good" quality based on  overall high amplitude data points [0.1].

    overall_Bad_Cutoff : float
                    cutoff for "Bad" quality based on overall high amplitude data point [0.2].

    time_Good_Cutoff : float
                    cutoff for "Good" quality based on time points of high variance across channels [0.1].

    time_Bad_Cutoff : float
                    cutoff for "Bad" quality based on time points of high variance across channels [0.2].

    bad_Channel_Good_Cutoff : float
                    cutoff for "Good" quality based on ratio of bad channels [0.15].

    bad_Channel_Bad_Cutoff : float
                    cutoff for "Bad" quality based on ratio of bad channels [0.3].

    channel_Good_Cutoff : float
                    cutoff for "Good" quality based on channels of high variance across time [0.15].

    channel_Bad_Cutoff : float
                    cutoff for "Bad" quality based on channels of high variance across time [0.3].

    Returns
    -------
    dataset_qualification : dict
                    a dictionary indicating is the dataset if "Good" = 100, "Regular" = 50 or "Bad" = 0.

    """
    # Check that the values in quality_metrics{} are positive numbers not equal to 0
    if (
        not isinstance(quality_metrics.values(), int)
        and not isinstance(quality_metrics.values(), float)
        or isinstance(quality_metrics.values(), bool)
        or (quality_metrics.values() <= 0)
    ):
        logger.error(
            "Some value of Quality Metrics is not a number, please verify your EEG input data"
        )

    # Rating of EEG DATA according to the values of quality_metrics
    # The function rates the EEG DATA with the rule that the rating depends on the WORST rating
    if (
        quality_metrics["overall_high_amp"] > overall_Bad_Cutoff
        or quality_metrics["times_high_var"] > time_Bad_Cutoff
        or quality_metrics["ratio_bad_chans"] > bad_Channel_Bad_Cutoff
        or quality_metrics["chan_high_var"] > channel_Bad_Cutoff
    ):
        dataset_qualification = {
            "dataset_qualification": 0
        }  # Bad EEG dataset rating if any rating is BAD
        return dataset_qualification
    elif (
        quality_metrics["overall_high_amp"] < overall_Good_Cutoff
        and quality_metrics["times_high_var"] < time_Good_Cutoff
        and quality_metrics["ratio_bad_chans"] < bad_Channel_Good_Cutoff
        and quality_metrics["chan_high_var"] < channel_Good_Cutoff
    ):
        dataset_qualification = {
            "dataset_qualification": 100
        }  # Good EEG dataset rating if all ratings are GOOD
        return dataset_qualification
    else:
        dataset_qualification = {
            "dataset_qualification": 50
        }  # Regular EEG dataset rating if any rating is REGULAR
        return dataset_qualification
