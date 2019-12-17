# from typing import List
import json
import logging
import os

import mne
import mne_bids
from matplotlib import pyplot as plt
from mne_bids.read import _read_raw, read_raw_bids
from mne_bids.utils import _parse_bids_filename, _write_json

from pyautomagic.preprocessing.preprocess import Preprocess as execute_preprocess
from pyautomagic.src.calcQuality import calcQuality
from pyautomagic.src.rateQuality import rateQuality

logger = logging.getLogger(__name__)
logger.setLevel(level=10)


class Block:
    """
    Object for all operations on an individual dataset.

    Initialized using the name and path of the raw data.
    Preprocess, interpolate, rate for quality, and store those files.

    Parameters
    ----------
    root_path: str
        root directory of the BIDS project
    data_filename: str
        BIDS filename with extension
    project: object
        project object to which this block belongs
    subject: object
        subject object to which this block belongs

    Attributes
    ----------
    unique_name : str
        raw file name minus extension, used for saving results as well
    file_ext : str
        raw file extension
    params : dict
        parameters for preprocessing and calculating quality metrics
    sampling_rate :
        sampling rate of raw data file
    result_path : str
        directory path to where results are stored for the block
    rate : str
        current rating of the file (good, bad, ok, not rated)
    to_be_interpolated : list
        list of channel indices that are to be interpolated
    auto_bad_chans : list
        list of channel indices detected as bad
    final_bad_chans : list
        list of channel indices determined to be bad after checks
    quality_scores : dict
        contains all metrics of quality calculated for the dataset
    times_committed : int
        used to track how many changes were made to the evaluation of the data
    Methods
    -------
    preprocess()
        run the block through preprocessing steps, calc quality scores, save files, write log
    interpolate()
        interpolate the dataset, update quality scores and rating, save files, write log
    """

    def __init__(self, root_path, data_filename, project, subject):
        self.root_path = root_path
        self.project = project
        self.subject = subject
        self.montage = project.montage  # could be switched to allow for ind.
        self.unique_name = os.path.splitext(data_filename)[0]
        self.file_ext = os.path.splitext(data_filename)[1]
        self.params = project.params
        self.sampling_rate = project.sampling_rate
        self.visualization_params = project.visualization_params
        self.result_path = self.find_result_path()
        self.is_rated = False
        self.is_interpolated = False
        self.times_committed = -1
        self.update_rating_from_file()
        self.rate = "not rated"
        self.index = -1
        # self.auto_bad_chans = []

    def update_rating_from_file(self):
        """
        Updates block information from the file currently stored

        Checks for results file, if it's there, and informaation, we update.
        No direct returns, but updates block fields.

        Parameters
        ----------
        none

        Returns
        -------
        none

        """
        result_filename = self.unique_name + "_results.json"
        result_file_overall = os.path.join(self.result_path, result_filename)
        if os.path.isfile(result_file_overall):
            with open(result_file_overall) as json_file:
                block = json.load(json_file)
            saved_params = block["params"]
            if not saved_params == self.params:
                raise ValueError(
                    "Parameters of results file do not match this project. Can not merge."
                )
            if block["is_interpolated"] or block["is_rated"]:
                self.rate = block["rate"]
                self.to_be_interpolated = block["to_be_interpolated"]
                self.is_interpolated = block["is_interpolated"]
                self.auto_bad_chans = block["auto_bad_chans"]
                self.final_bad_chans = block["final_bad_chans"]
                self.quality_scores = block["quality_scores"]
                self.times_committed = block["times_committed"]
            else:
                self.rate = "not rated"
                self.to_be_interpolated = []
                self.is_interpolated = False
                self.auto_bad_chans = []
                self.final_bad_chans = []
                self.quality_scores = None
                self.times_committed = int(0)

    def find_result_path(self):
        """
        Identifies the directory path pointing to where results stored

        Following BIDS requirements, we only have either the subject folder or both subject and session.

        Parameters
        ----------
        none

        Returns
        -------
        result_path: str
            location of results files within BIDS folder

        """
        params = _parse_bids_filename(self.unique_name, verbose=False)
        if params["ses"] is None:
            result_path = os.path.join(
                self.root_path, "derivatives", "automagic", f"sub-{params['sub']}"
            )
        else:
            result_path = os.path.join(
                self.root_path,
                "derivatives",
                "automagic",
                f"sub-{params['sub']}",
                f"ses-{params['ses']}",
            )
        return result_path

    def preprocess(self):
        """
        Preprocesses the raw data associated with this block

        Parameters
        ----------
        none

        Returns
        -------
       results: dict
            dictionary containing all the new updates to the block and the preprocessed array

        """
        data = self.load_data()
        self.params["line_freqs"] = data.info["sfreq"]
        self.params["interpolation_params"]["line_freqs"] = data.info["sfreq"]
        self.params["interpolation_params"]["ref_chs"] = data.ch_names
        self.params["interpolation_params"]["reref_chs"] = data.ch_names
        preprocess = execute_preprocess(data, self.params)
        preprocessed, fig_1, fig_2 = preprocess.fit()
        overall_thresh = self.project.quality_thresholds["overall_thresh"]
        time_thresh = self.project.quality_thresholds["time_thresh"]
        chan_thresh = self.project.quality_thresholds["chan_thresh"]
        apply_common_avg = self.project.quality_thresholds["apply_common_avg"]
        automagic = preprocess.automagic
        preprocessed.info["bads"] = automagic["auto_bad_chans"]
        quality_scores = calcQuality(
            preprocessed.get_data(),
            preprocessed.info["bads"],
            overall_thresh,
            time_thresh,
            chan_thresh,
            apply_common_avg,
        )
        # self.detected_bads = preprocessed['auto_bad_chans']
        update_to_be_stored = {
            "rate": "not rated",
            "is_manually_rated": False,
            "to_be_interpolated": automagic["auto_bad_chans"],
            "final_bad_chans": [],
            "is_interpolated": False,
            "quality_scores": quality_scores,
            "commit": True,
        }
        self.update_rating(update_to_be_stored)
        automagic.update(
            {
                "to_be_interpolated": automagic["auto_bad_chans"],
                "final_bad_chans": self.final_bad_chans,
                "montage": self.montage,
                "version": self.project.CGV.VERSION,
                "quality_scores": self.quality_scores,
                "quality_thresholds": self.project.quality_thresholds,
                "rate": self.rate,
                "is_manually_rated": self.is_manually_rated,
                "times_committed": self.times_committed,
                "params": self.params,
                "is_interpolated": self.is_interpolated,
                "is_rated": self.is_rated,
            }
        )
        results = {"preprocessed": preprocessed, "automagic": automagic}
        self.save_all_files(results, fig_1, fig_2)
        self.write_log(automagic)
        return results

    def load_data(self):
        """
        Load raw data from BIDS folder

        Allowing for a number of extensions, loads file

        Parameters
        ----------
        none

        Returns
        -------
        raw MNE object

        """
        # params = _parse_bids_filename(self.unique_name, verbose=False)
        # if params['ses'] is None :
        # bids_root = os.path.join(self.root_path,f"sub-{params['sub']}")
        # else:
        # bids_root = os.path.join(self.root_path,f"sub-{params['sub']}",f"ses-{params['ses']}")
        # data_path = os.path.join(bids_root,self.unique_name)
        bids_fname = self.unique_name + self.file_ext
        data = read_raw_bids(bids_fname, self.root_path)
        return data

    def update_rating(self, update):
        """
        Takes update about ratings and stores in object

        From project level object, get an update on rating info.

        Parameters
        ----------
        update : dict
            dictionary of updates

        Returns
        -------
        none
        """
        # update can have many fields, go through and see what they are and update the block accordingly
        if "quality_scores" in update:
            self.quality_scores = update["quality_scores"]
        if "rate" in update:
            self.rate = update["rate"]
            if not self.rate == "interpolate" and not "to_be_interpolated" in update:
                self.to_be_interpolated = []
        if "is_manually_rated" in update:
            overall_Good_Cutoff = self.project.rate_cutoffs["overall_Good_Cutoff"]
            overall_Bad_Cutoff = self.project.rate_cutoffs["overall_Bad_Cutoff"]
            time_Good_Cutoff = self.project.rate_cutoffs["time_Good_Cutoff"]
            time_Bad_Cutoff = self.project.rate_cutoffs["time_Bad_Cutoff"]
            bad_Channel_Good_Cutoff = self.project.rate_cutoffs[
                "bad_Channel_Good_Cutoff"
            ]
            bad_Channel_Bad_Cutoff = self.project.rate_cutoffs["bad_Channel_Bad_Cutoff"]
            channel_Good_Cutoff = self.project.rate_cutoffs["channel_Good_Cutoff"]
            channel_Bad_Cutoff = self.project.rate_cutoffs["channel_Bad_Cutoff"]
            this_rate = rateQuality(
                self.quality_scores,
                overall_Good_Cutoff,
                overall_Bad_Cutoff,
                time_Good_Cutoff,
                time_Bad_Cutoff,
                bad_Channel_Good_Cutoff,
                bad_Channel_Bad_Cutoff,
                channel_Good_Cutoff,
                channel_Bad_Cutoff,
            )
            if update["is_manually_rated"] and not update["rate"] == this_rate:
                self.is_manually_rated = True
            elif not update["is_manually_rated"]:
                self.is_manually_rated = False
        if "to_be_interpolated" in update:
            self.to_be_interpolated = update["to_be_interpolated"]
            if not update["to_be_interpolated"] == []:
                self.rate = "interpolate"
        if "final_bad_chans" in update:
            if update["final_bad_chans"] == []:
                self.final_bad_chans = update["final_bad_chans"]
            else:
                self.final_bad_chans.extend(update["final_bad_chans"])
        if "is_interpolated" in update:
            self.is_interpolated = update["is_interpolated"]
        if "commit" in update and update["commit"] == True:
            self.times_committed += 1

        self.project.update_rating_lists(self)

    def save_all_files(self, results, fig1, fig2):
        """
        Save results dictionary and figures to results path

        Parameters
        ----------
        results:
            MNE raw object with info attribute containing
        fig1:
            Figure of ??

        fig2:
            Figure of ??

        Returns
        -------
        none

        """
        main_result_file = results["automagic"]
        result_filename = self.unique_name + "_results.json"
        result_file_overall = os.path.join(self.result_path, result_filename)
        _write_json(result_file_overall, main_result_file, overwrite=True, verbose=True)
        processed = results["preprocessed"]
        processed_filename = self.unique_name + "_raw.fif"
        processed_file_overall = os.path.join(self.result_path, processed_filename)
        processed.save(processed_file_overall, overwrite=True)

        plt.figure(fig1.number)
        fig1_name = self.unique_name + ".png"
        fig1_name_overall = os.path.join(self.result_path, fig1_name)
        plt.savefig(fig1_name_overall, dpi=200)
        plt.figure(fig2.number)
        fig2_name = self.unique_name + "_orig.png"
        fig2_name_overall = os.path.join(self.result_path, fig2_name)
        plt.savefig(fig2_name_overall, dpi=100)

    def write_log(self, updates):
        """
        Writes a log for all of the updates its making/actions performed
        Parameters
        ----------
        updates: dict

        Returns
        -------
        Updates in log file

        """
        logger.log(20, f"pyautomagic version {self.project.CGV.VERSION}")
        logger.log(
            20,
            f"Project:{self.project.name}, Subject:{self.subject.name}, File: {self.unique_name}",
        )
        if "prep" in updates and updates["prep"]["performed"]:
            logger.log(20, "PREP performed.")
        if "crd" in updates and updates["crd"]["performed"]:
            logger.log(20, "CRD performed.")
        if "filtering" in updates and updates["filtering"]["performed"]:
            logger.log(20, "Filtering performed.")
        if "auto_bad_chans" in updates:
            logger.log(
                20,
                f'There were {len(updates["auto_bad_chans"])} bad channels detected.',
            )
        if "eog_regression" in updates and updates["eog_regression"]["performed"]:
            logger.log(20, "EOG regression performed.")
        logger.log(20, "Remove DC offset by subtracting the channel mean")
        if (
            "high_var_rejection" in updates
            and updates["high_var_rejection"]["performed"]
        ):
            logger.log(20, "Identify remaining noisy or outlier channels.")
        if "interpolation" in updates:
            logger.log(20, "Interpolate bad channels.")
        # TODO: fill the logger out more

    def interpolate(self):
        """
        Interpolates bad channels to create new data and updates info

        Parameters
        ----------
        none

        Returns
        -------
        none

        """
        result_filename = self.unique_name + "_results.json"
        result_file_overall = os.path.join(self.result_path, result_filename)
        processed_filename = self.unique_name + "_raw.fif"
        processed_file_overall = os.path.join(self.result_path, processed_filename)
        if os.path.isfile(result_file_overall) and os.path.isfile(
            processed_file_overall
        ):
            eeg = _read_raw(processed_file_overall)
            with open(result_file_overall) as json_file:
                automagic = json.load(json_file)
        else:
            raise (ValueError, "The block has not been preprocessed yet.")
            return
        interpolate_chans = self.to_be_interpolated
        if interpolate_chans == []:
            raise (
                ValueError,
                "The block is rated to be interpolated but no channels chosen",
            )
            return
        if (
            self.params == []
            or not "interpolation_params" in self.params
            or self.params["interpolation_params"] == []
        ):
            default_params = self.config["default_params"]
            interpolation_params = default_params["interpolation_params"]
        else:
            interpolation_params = self.params["interpolation_params"]
        eeg.load_data()
        eeg.info["dig"] = mne.channels.make_standard_montage(self.montage)
        interpolated = eeg.interpolate_bads()  # (origin=interpolation_params['origin'])

        overall_thresh = self.project.quality_thresholds["overall_thresh"]
        time_thresh = self.project.quality_thresholds["time_thresh"]
        chan_thresh = self.project.quality_thresholds["chan_thresh"]
        apply_common_avg = self.project.quality_thresholds["apply_common_avg"]
        quality_scores = calcQuality(
            interpolated.get_data(),
            interpolate_chans,
            overall_thresh,
            time_thresh,
            chan_thresh,
            apply_common_avg,
        )
        update_to_be_stored = {
            "rate": "not rated",
            "is_manually_rated": False,
            "to_be_interpolated": [],
            "final_bad_chans": interpolate_chans,
            "is_interpolated": True,
            "quality_scores": quality_scores,
        }
        self.update_rating(update_to_be_stored)
        automagic.update(
            {
                "interpolation": {
                    "channels": interpolate_chans,
                    "params": interpolation_params,
                },
                "quality_scores": self.quality_scores,
                "rate": self.rate,
            }
        )
        results = {"preprocessed": interpolated, "automagic": automagic}
        self.write_log(automagic)
        automagic.update(
            {
                "to_be_interpolated": self.to_be_interpolated,
                "rate": self.rate,
                "quality_scores": self.quality_scores,
                "is_manually_rated": self.is_manually_rated,
                "is_interpolated": self.is_interpolated,
            }
        )
        main_result_file = results["automagic"]
        result_filename = self.unique_name + "_results.json"
        result_file_overall = os.path.join(self.result_path, result_filename)
        _write_json(result_file_overall, main_result_file, overwrite=True, verbose=True)
        processed = results["preprocessed"]
        processed.info["dig"] = None
        processed_filename = self.unique_name + "_raw.fif"
        processed_file_overall = os.path.join(self.result_path, processed_filename)
        processed.save(processed_file_overall, overwrite=True)
        return results
