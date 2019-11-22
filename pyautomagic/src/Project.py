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

import timeit
import time
import os
import logging
import json
import mne
from mne_bids.utils import _parse_bids_filename
from pyautomagic.src.Block import Blockass
from pyautomagic.src import Config

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)


class Project:
    """
    Object containing all methods for creating a new project

    Parameters
    ----------
    name
        The name of the project

    d_folder
        The folder where the raw data is stored

    file_ext
        File extension

    params
        The default parameters to be used

    visualisation_params
        The default visualisation parameters to be used


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

    CGV
        Constant Global Variables

    current
        The index of the current block


    """

    def __init__(self, name, d_folder, file_ext, params, v_params):

        self.name = name  # Project name
        self.data_folder = d_folder  # Data folder
        self.results_folder = self.set_results_folder(d_folder)  # Results folder, calls a function from Block
        #self.file_extenstion = file_ext  # File extension
        # self.params = params
        # self.v_params = v_params
        #self.mask = file_ext
        self.quality_thresholds = Config.DefaultVisualisationParameters.CALC_QUALITY_PARAMS
        self.ds_rate = Config.DefaultVisualisationParameters.DS_RATE
        self.rate_cutoffs = Config.DefaultVisualisationParameters.RATE_QUALITY_PARAMS
        self.config = Config
        self.params = Config.DefaultParameters
        self.v_params = Config.DefaultVisualisationParameters
        self.CGV = Config.ConstantGlobalValues

        self.set_name(name)
        self.set_data_folder(d_folder)


    def get_current_block(self):  # NEEDED
        """
        Returns the block pointed by the current index

        Parameters
        ----------
        none

        Returns
        -------
        block
            Current block

        """

        pass

    def get_next_index(self):  # NEEDED
        """
        Returns the index of the next block in the list

        Parameters
        ----------
        next_idx

        good_bool

        ok_bool

        bad_bool

        interpolate_bool

        not_rated_bool

        Returns
        -------
        next
            Next block index

        """
        pass

    def get_previous_index(self):  # NEEDED
        """
        Returns the index of the previous block in the list

        Parameters
        ----------
        next_idx

        good_bool

        ok_bool

        bad_bool

        interpolate_bool

        not_rated_bool

        Returns
        -------
        previous
            Previous block index

        """
        pass

    def preprocess_all(self):
        """
        Preprocess all files in the data folder of the project

        Parameters
        ----------
        none

        Returns
        -------
        none

        """

        if not (os.path.isdir(self.data_folder)):
            logging.log(40,
                        "No directory exists, please specify the correct data directory")  # Displays error message if no data directory found

        else:
            logging.log(20, "----- START PREPROCESSING -----")
            start_time = timeit.default_timer()  # Calculates start time = CPU time
            for i in range(0, len(self.block_list)):
                unique_name = self.block_list[i]
                block = self.block_map[unique_name]
                # subject_name = block.subject.name
                logging.log(20, "Processing file %s %s out of %s", block.unique_name, i + 1, (len(self.block_list)))

                # logging.log(20, "Processing file %s %s out of %s", 'Saul', i+1, (len(self.block_list)))

                pX = Blockass()
                presults = pX.preprocess()

                EEG = presults['preprocessed']

                if not EEG:
                    logging.log(40, "EEG PREPROCESSED DATA NOT FOUND")
                    break

                # if self.current == -1:
                #   self.current = 1

                self.save_project()  # FUNCTION TO SAVE THE PROJECT
                logging.log(20, "**Project saved**")
                # time.sleep(1) #DELETE THIS LINE IS JUST TO CHECK THE TIME
            end_time = timeit.default_timer()  # Calculates end time
            logging.log(20, "---- PREPROCESSING FINISHED ----")
            logging.log(20, "Total elapsed time: %s sec",
                        end_time - start_time)  # Prints total elapsed time of the process

    def interpolate_selected(self):
        """
        Interpolates all the channels selected to be interpolated

        Parameters
        ----------
        none

        Returns
        -------
        none

        """

        if len(self.interpolate_list) == 0:  # Need to find interpolate_list
            logging.log(40, "Interpolate subjects list is empty, please rate first")

        else:
            logging.log(20, "----- START INTERPOLATION -----")
            start_time = timeit.default_timer()
            int_list = self.interpolate_list
            for i in range(0, len(int_list)):
                index = int_list[i]
                unique_name = self.block_list[index]
                block = self.block_map[unique_name]

                logging.log(20, "Processing file %s file %s out of %s", block.uniqueName, i + 1,
                            (len(self.interpolate_list)))

                iX = Blockass()
                iresults = iX.interpolate()

                self.already_interpolated = [self.already_interpolated, index]

                self.save_project()  # Method in this class to save the project
                logging.log(20, "**Project saved**")

            end_time = timeit.default_timer()  # Calculates end time
            logging.log(20, "----- INTERPOLATION FINISHED -----")
            logging.log(20, "Total elapsed time: %s sec",
                        start_time - end_time)  # Prints total elapsed time of the process

    def update_rating_lists(self, block_rate: str):  # NEEDED for Claire
        """
        Updates the five rating lists depending on the rating of the
        given block

        Parameters
        ----------
        block_rate : str

        Returns
        -------
        none

        """
        # block_rate = Config.ConstantGlobalValues.RATINGS

        pass

    def update_rating_structure(self):  # NEEDED 300 LINES OF CODE IN MATLAB
        """
        Updates the data structures of this project

        Parameters
        ----------
        none

        Returns
        -------
        none

        """
        pass

    def get_quality_ratings(self):  # NEEDED
        """
        Returns the quality ratings of all blocks given the cuttoffs

        Parameters
        ----------
        cutoffs : int
            The cutoffs for which the quality ratings are returned

        Returns
        -------
        ratings
            Quality ratings returned

        """
        pass
        # Method returns the quality ratings of all blocks

    def apply_quality_ratings(self, cutoffs, apply_to_manually_rated):  # NEEDED
        """
        Modify all the blocks to have the new ratings given by this
        cutoffs

        Parameters
        ----------
        cutoffs

        apply_to_manually_rated

        Returns
        -------
        none

        """
        pass
        # Modify all the blocks to have the new ratings given by this cutoffs

    def update_addresses_from_state_file(self, p_folder, data_folder):  # NOT NEEDED I THINK
        """
        Method called when the project is loaded from a state file

        Parameters
        ----------
        p_folder

        data_folder

        Returns
        -------
        none

        """
        pass
        # This method is called only when the project is loaded
        # from a state file

    def get_rated_count(self, rated_count):  # DEEP
        """
        Return number of files that have already been rated

        Parameters
        ----------
        none

        Returns
        -------
        rated_count : int
            Number of files that have been rated

        """
        pass

    def to_be_interpolated(self, count):  # Deep
        """
        Return the number of files that are rated as interpolate

        Parameters
        ----------
        none

        Returns
        -------
        count : int
            Number of files that are rated as interpolate

        """
        pass

    def are_folders_changed(self, modified):  # Deep
        """
        Method that verifies if any change has happened to data folder or results folder
        since the last update

        Parameters
        ----------
        none

        Returns
        -------
        modified : bool
            Returns true or false depending if the folders have been changed or not

        """
        pass

    def Export_To_BIDS(self):  # NOT NEEDED
        pass

    def save_project(self):  # DEEP
        """
        Save the class to the state file

        Parameters
        ----------
        none

        Returns
        -------
        none

        """
        pass
        # WRITE JSON
        # numpy.save(self.stateAddress)
        # Save the class to the state file
        # We need the state Adress to implement this function
        # Make_State_Address method is needed to get the address of the state file

    def list_subject_files(self):
        """
        Method that lists all folders in the data folder

        Parameters
        ----------
        None

        Returns
        -------
        lista : list
            List of all folders in the data folder

        """
        lista = self.list_subjects(self.data_folder)
        return lista

    def list_preprocessed_subjects(self):
        """
        Method that lists all folders in the results folder

        Parameters
        ----------
        none

        Returns
        -------
        lista : list
            List of all folders in the results folder
        """
        lista = self.list_subjects(self.results_folder)
        return lista

    def create_ratings_structure(self):
        """
        Method that creates and initialises all data structures based on the data
        on both data folder and results folder

        Parameters
        ----------
        none

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

        logging.log(20, 'Setting up project. Please wait...')
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

        for i in range(1, len(subjects)):
            subject_name = subjects[i]
            logging.info('Adding subject %s', subject_name)
            subject = Subject([self.data_folder, subject_name, self.results_folder, subject_name])
            raw_files = self.dir_not_hiddens(self.data_folder)  # Fill here with the data folder
            temp = 0
            files_count = 0
            for j in range(1, len(raw_files)):
                files_count = files_count + 1
                file = raw_files[j]
                file_path = []  # Fill here with the file folder of the raw file
                name_temp = file.name

                splits = os.path.splitext(name_temp)
                file_name = splits[1]
                logging.info('...Adding file %s', file_name)

                mapa[block.unique_name] = block  # unique_name from block is needed
                listb[files_count] = block.unique_name
                block.index = files_count

                if block.is_interpolated:
                    already_list = [already_list, block.index]

                p_list.append(block.unique_name)  # block.unique_name
                n_preprocessed_file = n_preprocessed_file + 1
                temp = temp + 1

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

        if not self.processed_list:
            self.current = 1
        else:
            self.current = -1

        self.save_project()

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

    def set_data_folder(self, data_folder):
        """
        Sets the path folder where the data is stored

        Parameters
        ----------
        data_folder

        Returns
        -------
        self.data_folder : str
            Path to the data folder

        """
        self.data_folder = data_folder
        if not os.path.exists(self.data_folder):
            logging.error("This folder doesn't exist, please verify the path and enter the correct one")
        else:
            print("this exists!: ", self.data_folder)
            return self.data_folder

    def set_results_folder(self, folder):

        """
        Sets the path folder where the results will be stored

        Parameters
        ----------
        folder
            Path where is the data stored

        Returns
        -------
        self.results_folder
            Path to the results folder

        """
        self.results_folder = os.path.join(folder, 'derivatives', 'automagic')
        print(self.results_folder)
        return self.results_folder

    def check_existings(self):  # NOT NEEDED
        pass
        # If there is already one preprocessed file in the resutlts folder
        # ask the user to overwrite the file or skip it

    def write_to_log(self, source_address, msg):  # M N D U
        """
        Method that writes specal events that happened during preprocessing
        into the log file

        Parameters
        ----------
        source_address : file
            The block file for which the error is printed

        Returns
        -------
        msg : str
            The message to be written in the log file

        """
        pass
        # Write special events that happened during preprocessing into
        # the log file

    def update_main_gui(self):  # NOT NEEDED
        pass

    @staticmethod
    def add_slash(folder):  # NOT NEEDED
        pass

    @staticmethod
    def add_automagic_paths():  # NOT NEEDED
        pass

    @staticmethod
    def make_state_address(p_folder):  # NOT NEEDED
        pass

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
            rate = 'Manually Rated'
        else:
            rate = q_rate
        return rate

    @staticmethod
    def list_subjects(root_folder):

        """
        Returns the list of subjects in the folder

        Parameters
        ----------
        root_folder
            The folder in which the subjects are looked for

        Returns
        -------
        subjects : object
            Subjects in the root folder
        """

        if os.path.isdir(root_folder):
            subs = os.path.join(root_folder)
            subjects = [y for y in os.listdir(subs) if os.path.isdir(os.path.join(root_folder, y))]
            #print(subjects)
            return subjects
        else:
            logging.log(30, "No directory exists")

    @staticmethod
    def dir_not_hiddens(folder):
        """
        Returns the list of files in the folder, excluding the hidden files

        Parameters
        ----------
        folder
            The folder in which the files are listed

        Returns
        -------
        subjects
            List of files that are not hidden

        """
        subs = os.path.join(folder)
        files = [y for y in os.listdir(subs) if os.path.isfile(y)]
        return files

    @staticmethod
    def is_folder_changed(folder, folder_counts, n_blocks, ext, all_steps):  # NOT NEEDED
        pass


# DUMMY DATA TO TEST THE PROJECT CLASS, THIS WILL BE DELETED

#X = Project("Saul", "C:/Users\saul__000\OneDrive\Escritorio\Johns Hopkins", ".mat", "C:/Users\saul__000\OneDrive\Escritorio\Johns Hopkins", "A", "B")
#Y = X.set_data_folder("C:/Users\saul__000\OneDrive\Escritorio\Johns Hopkins")

