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

import time
import os
import logging
import numpy as np
import json

from pyautomagic.src import Config

logger = logging.getLogger(__name__)


class Project:
    """
    Object containing all methods for creating a new project

    Parameters
    ----------
    name : str

    data_folder : str

    results_folder : str

    file_extension : str

    preprocess_parameters : dict

    visualisation_parameters : dict


    Attributes
    ----------



    """

    def __init__(self, name: str, data_folder: str, results_folder: str, file_extension: str,
                 preprocess_parameters: dict, visualisation_parameters: dict):

        self.set_name(name)
        self.set_data_folder()
        self.set_results_folder()
        self.create_ratings_stuctures()
     #  self.mask = ext  # Method needed
        self.quality_thresholds = Config.DefaultVisualisationParameters.CALC_QUALITY_PARAMS # Needed
        self.ds_rate = Config.DefaultVisualisationParameters.DS_RATE
        self.quality_cutoffs = Config.DefaultVisualisationParameters.RATE_QUALITY_PARAMS

        params = Config.DefaultParameters
        v_params = Config.DefaultVisualisationParameters

        self.name = name
        self.data_folder = data_folder
        self.results_folder = results_folder
        self.file_extension = file_extension
        self.preprocess_parameters = preprocess_parameters
        self.visualisation_parameters = visualisation_parameters

        self.params = params # Default Parameters
        self.v_params = v_params # Default Visualisation Parameters

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

    def set_data_folder(self):
        """
        Sets the path folder where the data is stored

        Parameters
        ----------
        none

        Returns
        -------
        self.data_folder : str
            Path to the data folder

        """
        self.data_folder = input("Please enter the path to the data folder: ")  # Asks the user to type the data folder path
        if not os.path.exists('self.data_folder'):
            logger.error("This folder doesn't exist, please verify the path and enter the correct one")
        else:
            return self.data_folder

    def set_results_folder(self):
        """
        Sets the path folder where the results will be stored

        Parameters
        ----------
        none

        Returns
        -------
        self.results_folder : str
            Path to the results folder

        """
        self.results_folder = input(
            "Please enter the path where you want your results: ")  # Asks the user to type the results folder path
        os.mkdir(self.results_folder) # Makes directory for results
        return self.results_folder

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
            logger.error(
                "No directory exists, please specify the correct data directory")  # Displays error mesagge if no data directory found
        else:
            logger.log(20, "----- START PREPROCESSING -----")
            start_time = time.process_time()  # Calculates start time = CPU time
            for i in range(1, len(self.blockList)): # blockList needed from Block class
                uniqueName = self.blockList[i] # blockList needed from Block class
                block = self.blockMap(uniqueName) # blockMap needed from Block class
                block.updateAddresses(self.data_folder, self.results_folder, self.params.EEG_SYSTEM['locFile']) # updateAddresses needed from Block class

                print("Processing file ", block.uniqueName, " file ", i, " out of ", (len(self.blockList))) # We need uniqueName and blockList

                [EEG] = block.preprocess()  # Call preprocess function to preprocess EEG data, needed from Block class

                if len(EEG) == 0:
                    logger.error("ERROR: EEG DATA NOT FOUND")

                self.save_project()  # Function to save the project

            end_time = start_time - time.process_time()  # Calculates end time
            logger.log(20, "----- PREPROCESSING FINISHED -----")
            logger.info("Total elapsed time: ", end_time)  # Prints total elapsed time of the process

    def interpolate_selected(self):
        """
        Interpolates all the channels selected

        Parameters
        ----------
        none

        Returns
        -------
        none

        """
        if len(self.interpolate_list) == 0:  # Need to find interpolate_list
            logger.error("Interpolate subjects list is empty, please rate first")

        else:
            logger.log(20, "----- START INTERPOLATION -----")
            start_time = time.process_time()  # Calculates start time = CPU time
            for i in range(1, len(self.interpolate_list)):
                uniqueName = self.blockList[i] # Whats block list?
                block = self.blockMap(uniqueName) #Whats block map?
                block.updateAddresses(self.data_folder, self.results_folder, self.params.EEGSystem.locFile)

                print("Processing file ", block.uniqueName, " file ", i, " out of ", (len(self.interpolate_list)))

               # block.interpolate()

               # self.alreadyInterpolated = [self.alreadyInterpolated, i]

                self.save_project() # Method in this class to save the project

            end_time = start_time - time.process_time()  # Calculates end time
            logger.log(20, "----- INTERPOLATION FINISHED -----")
            logger.info("Total elapsed time: ", end_time)  # Prints total elapsed time of the process

    def get_current_block(self): # NEEDED
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

    def get_next_index(self): # NEEDED
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

    def get_previous_index(self): # NEEDED
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

    def update_rating_lists(self, block_rate: str): # NEEDED for Claire
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
        #block_rate = Config.ConstantGlobalValues.RATINGS

        if block_rate == 'Good':
            # Do something
            pass
        elif block_rate == 'Ok':
            # Do something
            pass
        elif block_rate == 'Bad':
            # Do something
            pass
        elif block_rate == 'Interpolate':
            # Do something
            pass
        elif block_rate == 'Not Rated':
            # Do something
            pass

    def update_rating_structure(self): # NEEDED 300 LINES OF CODE IN MATLAB
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

    def get_quality_ratings(self, cutoffs: float): # NEEDED
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

    def apply_quality_ratings(self, cutoffs, apply_to_manually_rated): # NEEDED
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

    def get_rated_count(self, rated_count): #Deep
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

    def to_be_interpolated(self, count): #Deep
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

    def are_folders_changed(self, modified): #Deep
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

    def Export_To_BIDS(self): #NOT NEEDED
        pass

    def save_project(self): # M N D U
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

    def list_subject_files(self): # MAYBE NEEDED
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
        #lista  = os.listdir(self.data_folder)
        lista = self.list_subjects(self.data_folder)
        return lista

    def list_preprocessed_subjects(self):  # MAYBE NEEDED
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
        #lista = os.listdir(self.results_folder)
        lista = self.list_subjects(self.results_folder)
        return lista

    def create_ratings_structure(self, ):  # NEEDED
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
        pass
        logger.log(20, 'Setting up project. Please wait...')
        modified = False
        subjects = os.listdir(self.data_folder) #
        s_count = len(subjects)#Verify the error

        map = {}
        lista = np.empty(0) # lista from list_subject_files()
        p_list = np.empty(0)
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
            # CONTINUE HERE...


    def check_existings(self, skip): # NOT NEEDED
        pass
        #If there is already one preprocessed file in the resutlts folder
        #ask the user to overwrite the file or skip it

    def write_to_log(self, source_address, msg): # M N D U
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

    def update_main_gui(self): #NOT NEEDED
        pass

    def add_slash(self, folder): #NOT NEEDED
        pass

    def add_automagic_paths(self): #NOT NEEDED
        pass

    def make_state_address(self, address): #NOT NEEDED
        pass

    def make_rating_manually(self, q_rate): #Deep
        """
        Returns q_rate if the block is not rated manually.

        Parameters
        ----------
        q_rate : float
            The rate to be returned

        Returns
        -------
        none

        """
        pass

    @staticmethod
    def list_subjects(rootFolder):
        """
        Returns the list of subjects in the folder

        Parameters
        ----------
        rootFolder
            The folder in which the subjects are looked for

        Returns
        -------
        subjects : object
            Subjects in the root folder
        """

        subs = os.path.join(rootFolder)
        subjects = [y for y in os.listdir(subs) if os.path.isdir(y)]
        return subjects

    #     #subjects = os.listdir(rootFolder) ***SAUL
    #
    #     for file in os.listdir(rootFolder):
    #         if os.path.isfile(os.path.join(root_folder, file)):
    #             yield file

    def dir_not_hiddens(self, folder): #Deep
        """
        Returns the list of files in the folder, excluding the hidden files

        Parameters
        ----------
        folder
            The folder in which the files are listed

        Returns
        -------
        files
            List of files that are not hidden

        """
        pass

    def is_folder_changed(self, modified): #NOT NEEDED
        pass
