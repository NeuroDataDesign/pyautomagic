import numpy as np
import timeit
import os
import logging
import mne
import mne_bids
from mne_bids.utils import _write_json
from pyautomagic.src.rateQuality import rateQuality
from pyautomagic.src.Block import Block
from pyautomagic.src.Subject import Subject
from pyautomagic.src import Config

logging.basicConfig(
    format="%(asctime)s - %(levelname)s: %(message)s", level=logging.DEBUG
)


class Project:
    """
    Object containing all methods for creating a new project.


    Parameters
    ----------
    name : str
        The name of the project

    d_folder : str
        The folder where the raw data is stored

    file_ext : str
        File extension

    montage : str
        Montage to be used

    sampling_rate : int
        Sampling rate for the txt file

    params : dict
        Preprocessing parameters for the new project


    Attributes
    ----------
    quality_thresholds
        The thresholds to rate te quality of the datasets

    ds_rate
        Sampling rate to create reduced files

    rate_cutoffs
        Sampling rate to the recorded data

    config
        Configuration file with all the project constants

    params : dir
        The default parameters to be used

    visualization_params : dir
        The default visualisation parameters to be used

    CGV : dict
        Constant Global Variables

    """

    def __init__(self, name, d_folder, file_ext, montage, sampling_rate, params):

        self.name = self.set_name(name)
        self.data_folder = self.set_data_folder(d_folder)
        self.results_folder = self.set_results_folder(d_folder)
        self.file_extension = file_ext.partition(".")[2]
        self.mask = file_ext
        self.quality_thresholds = (
            Config.DefaultVisualizationParameters.CALC_QUALITY_PARAMS
        )
        self.ds_rate = Config.DefaultVisualizationParameters.DS_RATE
        self.rate_cutoffs = Config.DefaultVisualizationParameters.RATE_QUALITY_PARAMS
        self.config = Config
        self.params = params
        self.visualization_params = Config.DefaultVisualizationParameters
        self.CGV = Config.ConstantGlobalValues
        self.automagic_final = {}
        self.montage = montage
        self.sampling_rate = sampling_rate

        # Calling create_rating_structures() method
        self.create_ratings_structure()

    def get_current_block(self):
        """
        Returns the block pointed by the current index

        Parameters
        ----------
        None

        Returns
        -------
        block
            Current block

        """

        if self.current == -1:
            subject = Subject("")
            block = Block("", "", self, subject)
            block.index = -1
            return

        unique_name = self.processed_list[self.current]
        block = self.block_map[unique_name]
        return block

    def preprocess_all(self):
        """
        Preprocess all files in the data folder of the project

        Parameters
        ----------
        None

        Returns
        -------
        None

        """

        if not (os.path.isdir(self.data_folder)):
            logging.log(
                40, "No directory exists, please specify the correct data directory"
            )  # Displays error message if no data directory found

        else:
            logging.log(20, "----- START PREPROCESSING -----")
            start_time = timeit.default_timer()  # Calculates start time
            for i in range(0, len(self.block_list)):
                unique_name = self.block_list[i]
                block = self.block_map[unique_name]
                subject_name = block.subject.name
                logging.log(
                    20,
                    "Processing file %s %s out of %s",
                    block.unique_name,
                    i + 1,
                    (len(self.block_list)),
                )

                if not os.path.exists(
                    os.path.join(self.results_folder, "sub-" + subject_name)
                ):
                    os.makedirs(
                        os.path.join(self.results_folder, "sub-" + subject_name)
                    )

                p_results = block.preprocess()  # Preprocess function
                EEG = p_results["preprocessed"]
                if not EEG:
                    logging.log(40, "EEG PREPROCESSED DATA NOT FOUND")
                    break

                if self.current == -1:
                    self.current = 1

                self.update_project(p_results)  # Function to save the current changes
                logging.log(20, "**Project saved**")
            self.save_project()  # Function to save all the changes
            end_time = timeit.default_timer()  # End time
            logging.log(20, "---- PREPROCESSING FINISHED ----")
            logging.log(
                20, "Total elapsed time: %s sec", end_time - start_time
            )  # Prints total elapsed time of the process

    def interpolate_selected(self):
        """
        Interpolates all the channels selected to be interpolated

        Parameters
        ----------
        None

        Returns
        -------
        None

        """

        if len(self.interpolate_list) == 0:
            logging.log(40, "Interpolate subjects list is empty, please rate first")

        else:
            logging.log(20, "----- START INTERPOLATION -----")
            start_time = timeit.default_timer()
            int_list = self.interpolate_list
            for i in range(0, len(int_list)):
                index = int(int_list[i])
                unique_name = self.block_list[index - 1]
                block = self.block_map[unique_name]

                logging.log(
                    20,
                    "Processing file %s file %s out of %s",
                    block.unique_name,
                    i + 1,
                    (len(self.interpolate_list)),
                )

                block.interpolate()

                self.already_interpolated.append(index)

                logging.log(20, "**Project saved**")
            self.save_project()
            end_time = timeit.default_timer()  # Calculates end time
            logging.log(20, "----- INTERPOLATION FINISHED -----")
            logging.log(
                20, "Total elapsed time: %s sec", end_time - start_time
            )  # Prints total elapsed time of the process

    def update_rating_lists(self, block):
        """
        Updates the rating lists according to the rating of the block.

        Parameters
        ----------
        block
            block for which the rating list has to be updated

        Returns
        -------
        None

        """
        self.good_list = np.asarray(self.good_list)
        self.not_rated_list = np.asarray(self.not_rated_list)
        self.ok_list = np.asarray(self.ok_list)
        self.bad_list = np.asarray(self.bad_list)
        self.interpolate_list = np.asarray(self.interpolate_list)

        if block.rate == self.CGV.RATINGS["Good"]:
            if not np.isin(block.index, self.good_list):
                self.good_list = np.append(self.good_list, block.index)
                self.not_rated_list = self.not_rated_list[
                    self.not_rated_list != block.index
                ]
                self.ok_list = self.ok_list[self.ok_list != block.index]
                self.bad_list = self.bad_list[self.bad_list != block.index]
                self.interpolate_list = self.interpolate_list[
                    self.interpolate_list != block.index
                ]
                self.good_list = np.unique(self.good_list)

        elif block.rate == self.CGV.RATINGS["OK"]:
            if not np.isin(block.index, self.ok_list):
                self.ok_list = np.append(self.ok_list, block.index)
                self.not_rated_list = self.not_rated_list[
                    self.not_rated_list != block.index
                ]
                self.good_list = self.good_list[self.good_list != block.index]
                self.bad_list = self.bad_list[self.bad_list != block.index]
                self.interpolate_list = self.interpolate_list[
                    self.interpolate_list != block.index
                ]
                self.ok_list = np.unique(self.ok_list)

        elif block.rate == self.CGV.RATINGS["Bad"]:
            if not np.isin(block.index, self.bad_list):
                self.bad_list = np.append(self.bad_list, block.index)
                self.not_rated_list = self.not_rated_list[
                    self.not_rated_list != block.index
                ]
                self.good_list = self.good_list[self.good_list != block.index]
                self.ok_list = self.ok_list[self.ok_list != block.index]
                self.interpolate_list = self.interpolate_list[
                    self.interpolate_list != block.index
                ]
                self.bad_list = np.unique(self.bad_list)

        elif block.rate == self.CGV.RATINGS["Interpolate"]:
            if not np.isin(block.index, self.interpolate_list):
                self.interpolate_list = np.append(self.interpolate_list, block.index)
                self.not_rated_list = self.not_rated_list[
                    self.not_rated_list != block.index
                ]
                self.good_list = self.good_list[self.good_list != block.index]
                self.ok_list = self.ok_list[self.ok_list != block.index]
                self.bad_list = self.bad_list[self.bad_list != block.index]
                self.interpolate_list = np.unique(self.interpolate_list)

        elif block.rate == self.CGV.RATINGS["NotRated"]:
            if not np.isin(block.index, self.not_rated_list):
                self.not_rated_list = np.append(self.not_rated_list, block.index)
                self.bad_list = self.bad_list[self.bad_list != block.index]
                self.good_list = self.good_list[self.good_list != block.index]
                self.ok_list = self.ok_list[self.ok_list != block.index]
                self.interpolate_list = self.interpolate_list[
                    self.interpolate_list != block.index
                ]
                self.not_rated_list = np.unique(self.not_rated_list)

        self.good_list = self.good_list.tolist()
        self.not_rated_list = self.not_rated_list.tolist()
        self.ok_list = self.ok_list.tolist()
        self.bad_list = self.bad_list.tolist()
        self.interpolate_list = self.interpolate_list.tolist()

    def get_quality_ratings(self, cutoffs):
        """
        Parameters
        ----------
        cutoffs : dict
            cutoffs on which the ratings will be decided

        Returns
        -------
        ratings : list
            list of block-wise ratings
        """

        blocks = [self.block_map[x] for x in self.processed_list]
        q_scores = [z.quality_scores for z in blocks]
        ratings = [rateQuality(w) for w in q_scores]
        return ratings

    def get_rated_count(self):
        """
        Parameters
        ----------
        None


        Returns
        -------
        Count for no. of blocks that are yet to be rated
        """
        return len(self.processed_list) - (
            len(self.not_rated_list) + len(self.interpolate_list)
        )

    def to_be_interpolated_count(self):
        """
        Parameters
        ----------
        None

        Returns
        -------
        Count for no. of blocks that are yet to be interpolated
        """
        return len(self.interpolate_list)

    def save_project(self):
        """
        saves the project information to a JSON file

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        result_file = self.name + "_results.json"
        result_file_path = os.path.join(self.results_folder, result_file)
        _write_json(
            result_file_path, self.automagic_final, overwrite=True, verbose=True
        )

    def update_project(self, preprocessed):
        """
        Updates the project information dictionary with each blocks information

        Parameters
        ----------
        preprocessed
            Preprocessed files

        Returns
        -------
        None
        """
        update = preprocessed["automagic"]
        self.automagic_final.update(update)

    def list_subject_files(self):

        """
        Method that lists all folders in the data folder

        Parameters
        ----------
        None

        Returns
        -------
        listb : list
            List of all folders in the data folder

        """
        listb = self.list_subjects(self.data_folder)
        return listb

    def list_preprocessed_subjects(self):
        """
        Method that lists all folders in the results folder

        Parameters
        ----------
        None

        Returns
        -------
        listb : list
            List of all folders in the results folder
        """
        listb = self.list_subjects(self.results_folder)
        return listb

    def create_ratings_structure(self):
        """
        Method that creates and initializes all data structures based on the data
        on both data folder and results folder

        Parameters
        ----------
        None

        Returns
        -------
        block_list
        processed_list
        block_map
        n_processed_subjects
        n_processed_files
        n_block
        current
        interpolate_list
        good_list
        bad_list
        ok_list
        not_rated_list

        """

        logging.log(20, "Setting up project. Please wait...")
        slash = os.path.sep
        subjects = self.list_subject_files()
        s_count = len(subjects)

        mapa = {}
        listb = []
        ext = self.file_extension
        p_list = []
        i_list = []
        g_list = []
        b_list = []
        o_list = []
        n_list = []
        already_list = []

        files_count = 0
        n_preprocessed_file = 0
        n_preprocessed_subject = 0

        for i in range(0, len(subjects)):
            subject_name = subjects[i]
            if not subject_name.startswith(
                "derivatives"
            ):  # Condition to exclude the results folder when looking for the subjects
                logging.info("Adding subject %s", subject_name)
                a = self.data_folder + slash + subject_name
                b = self.results_folder + slash + subject_name
                subject = Subject(a)
                raw_files = []
                sess_or_EEG = self.list_subjects(subject.data_folder)

                if (
                    len(sess_or_EEG) != 0
                    and any(i.startswith("ses-") for i in sess_or_EEG)
                    and all(i.startswith("ses-") for i in sess_or_EEG)
                ):
                    for sesIdx in range(0, len(sess_or_EEG)):
                        sess_file = sess_or_EEG[sesIdx]
                        eeg_fold = (
                            subject.data_folder
                            + slash
                            + sess_file
                            + slash
                            + "eeg"
                            + slash
                        )
                        if os.path.isdir(eeg_fold):
                            raw_files = raw_files.append(
                                self.dir_not_hiddens(eeg_fold, self.mask)
                            )

                elif (
                    len(sess_or_EEG) != 0
                    and any(i.startswith("ses-") for i in sess_or_EEG)
                    and any(i.startswith("eeg") for i in sess_or_EEG)
                ):
                    eeg_fold = subject.data_folder + slash + "eeg" + slash
                    raw_files = self.dir_not_hiddens(eeg_fold, self.mask)

                elif len(sess_or_EEG) != 0 and any(
                    i.startswith("eeg") for i in sess_or_EEG
                ):
                    eeg_fold = subject.data_folder + slash + "eeg" + slash
                    raw_files = self.dir_not_hiddens(eeg_fold, self.mask)

                else:
                    raw_files = self.dir_not_hiddens(a + slash, self.mask)

                temp = 0
                for j in range(0, len(raw_files)):
                    files_count = files_count + 1
                    file = raw_files[j]
                    name_temp = file.name
                    if not ext in name_temp:
                        if not ext.isupper():
                            ext = ext.upper()
                        elif not ext.islower():
                            ext = ext.lower()

                        self.mask = self.mask.replace(self.file_extension, ext)
                        self.file_extension = ext

                    file_name = name_temp
                    logging.info("...Adding file %s", file_name)

                    block = Block(
                        self.data_folder, file_name, self, subject
                    )  # Calling block class
                    mapa[block.unique_name] = block
                    listb.insert(files_count, block.unique_name)
                    block.index = files_count

                    if block.rate == "Good":
                        g_list.append(block.index)
                    elif block.rate == "OK":
                        o_list.append(block.index)
                    elif block.rate == "Bad":
                        b_list.append(block.index)
                    elif block.rate == "interpolate":
                        i_list.append(block.index)
                    elif block.rate == "not rated":
                        n_list.append(block.index)

                    if block.is_interpolated:
                        already_list.append(block.index)

                    p_list.append(block.unique_name)
                    n_preprocessed_file = n_preprocessed_file + 1
                    temp = temp + 1

                if len(raw_files) != 0 and temp == len(raw_files):
                    n_preprocessed_subject = n_preprocessed_subject + 1

        self.processed_list = p_list
        self.n_processed_files = n_preprocessed_file
        self.n_processed_subjects = n_preprocessed_subject
        self.n_block = files_count
        self.n_subject = s_count
        self.block_map = mapa
        self.block_list = listb
        self.interpolate_list = i_list
        self.good_list = g_list
        self.bad_list = b_list
        self.ok_list = o_list
        self.not_rated_list = n_list
        self.already_interpolated = already_list

        if len(self.processed_list) != 0:
            self.current = 1
        else:
            self.current = -1

        self.save_project()
        logging.info("**Project saved**")

    def set_name(self, name):
        """
        Sets the name of a new project

        Parameters
        ----------
        name : str
            Name of the current project

        Returns
        -------
        self.name : str
            Name of the new project

        """
        self.name = name
        return self.name

    def set_data_folder(self, folder):
        """
        Sets the path folder where the data is stored

        Parameters
        ----------
        folder : str
            Path to the raw data folder

        Returns
        -------
        self.data_folder : str
            Path to the raw data folder

        """
        self.data_folder = folder
        if not os.path.exists(self.data_folder):
            logging.error(
                "%s: This folder doesn't exist, please verify your data folder", folder
            )
        else:
            return self.data_folder

    def set_results_folder(self, folder):

        """
        Sets the path folder where the results will be stored

        Parameters
        ----------
        folder : str
            Path where is the data stored

        Returns
        -------
        self.results_folder : str
            Path to the results folder

        """
        if not os.path.exists(folder):
            logging.error(
                "%s: Cannot create results folder, please verify your data folder",
                folder,
            )
        else:
            self.results_folder = os.path.join(folder, "derivatives", "automagic")
            if not os.path.exists(self.results_folder):
                os.makedirs(self.results_folder)
            return self.results_folder

    @staticmethod
    def make_rating_manually(block, q_rate):
        """
        Returns q_rate if the block is not rated manually.

        Parameters
        ----------
        q_rate : float
            The rate to be returned
        block
            Block for which the rate is returned

        Returns
        -------
        rate
            Return q_rate if the block is not manually rated.
            If it is rated manually return 'Manually rated'

        """
        rate = None
        if block.is_manually_rated:
            rate = "Manually Rated"
        else:
            rate = q_rate
        return rate

    @staticmethod
    def list_subjects(root_folder):

        """
        Returns the list of subjects in the folder

        Parameters
        ----------
        root_folder : str
            The folder in which the subjects are looked for

        Returns
        -------
        subjects : list
            List of subjects in the root folder
        """

        subs = os.path.join(root_folder)
        subjects = [
            y for y in os.listdir(subs) if os.path.isdir(os.path.join(root_folder, y))
        ]
        if len(subjects) == 0:
            logging.error(
                "%s: This path doesn't have any folders, please verify your data",
                root_folder,
            )
        else:
            return subjects

    @staticmethod
    def dir_not_hiddens(folder, extn):
        """
        Returns the list of files in the folder, excluding the hidden files

        Parameters
        ----------
        folder
            The folder in which the files are listed

        extn
            Extension of the raw file

        Returns
        -------
        files
            List of files that are not hidden

        """
        files = []
        for f in os.scandir(folder):
            fname, fext = os.path.splitext(f.name)
            if os.path.isfile(os.path.join(folder, f.name)) and fext == extn:
                files.append(f)

        return files
