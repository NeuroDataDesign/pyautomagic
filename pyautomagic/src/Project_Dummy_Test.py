import timeit
import os
import logging
import ntpath
#import json
#import mne
#from pyautomagic.src import Config

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)

class Block:

    def __init__(self, data_name, data_folder):
        self.unique_name = data_name
        self.data_folder = data_folder
        self.subject = Subject('name', '')
        self.is_interpolated = False

    def preprocess(self):
        results = {'preprocessed': 'A' 'B' 'C'}
        return results
        pass

    def interpolate(self):
        pass

class Subject:

    def __init__(self, data_folder, result_folder):
        self.result_folder = result_folder
        self.data_folder = data_folder
        self.name = self.extract_name(data_folder)

    def update_addresses(self, new_data_path, new_project_path):
        """
            This method is to be called to update addresses
            in case the project is loaded from another operating system and may
            have a different path to the dataFolder or resultFolder. This can
            happen either because the data is on a server and the path to it is
            different on different systems, or simply if the project is loaded
            from a windows to a iOS or vice versa.
        """

        self.data_folder = ntpath.join(new_data_path, self.name)
        self.result_folder = ntpath.join(new_project_path, self.name)

    @staticmethod
    def extract_name(address):
        head, tail = ntpath.split(address)
        return tail or ntpath.basename(head)


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

    v_params
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

    def __init__(self, name, d_folder, file_ext):

        self.name = name  # Project name
        self.data_folder = d_folder  # Data folder
        self.results_folder = self.set_results_folder(d_folder)  # Results folder, calls a function from Block
        self.file_extension = os.path.splitext(file_ext)[1]  # File extension
        self.mask = file_ext

        self.set_name(name)
        self.set_data_folder(d_folder)

        # Dummy data to test functions
        self.block_list = ["Liang", "Deep", "Claire", "Raph", "Aamna"]
        self.block_map = {}
        for i in range(len(self.block_list)):
            self.block_map[self.block_list[i]] = Block(self.block_list[i], '')

        # More dummy data
        self.interpolate_list = [0, 1, 2, 3, 4]
        self.already_interpolated = [5]

    def preprocess_all_test(self):

        if not (os.path.isdir(self.data_folder)):
            logging.log(40,
                        "No directory exists, please specify the correct data directory")  # Displays error message if no data directory found

        else:
            logging.log(20, "----- START PREPROCESSING -----")
            start_time = timeit.default_timer()  # Calculates start time = CPU time
            for i in range(0, len(self.block_list)):
                unique_name = self.block_list[i]
                block = self.block_map[unique_name]
                subject_name = block.subject.name
                logging.log(20, "Processing file %s %s out of %s", block.unique_name, i + 1, (len(self.block_list)))

                if not os.path.exists(os.path.join(self.results_folder, subject_name)):
                    os.makedirs(os.path.join(self.results_folder, subject_name))

                presults = block.preprocess()
                EEG = presults['preprocessed']
                if not EEG:
                    logging.log(40, "EEG PREPROCESSED DATA NOT FOUND")
                    break

                self.save_project()  # FUNCTION TO SAVE THE PROJECT
                logging.log(20, "**Project saved**")
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

        if len(self.interpolate_list) == 0:
            logging.log(40, "Interpolate subjects list is empty, please rate first")

        else:
            logging.log(20, "----- START INTERPOLATION -----")
            start_time = timeit.default_timer()
            int_list = self.interpolate_list
            for i in range(0, len(int_list)):
                index = int_list[i]
                unique_name = self.block_list[index]
                block = self.block_map[unique_name]

                logging.log(20, "Processing file %s file %s out of %s", block.unique_name, i+1,
                            (len(self.interpolate_list)))

                block.interpolate()

                self.already_interpolated = [self.already_interpolated, index]

                self.save_project()  # Method in this class to save the project
                logging.log(20, "**Project saved**")

            end_time = timeit.default_timer()  # Calculates end time
            logging.log(20, "----- INTERPOLATION FINISHED -----")
            logging.log(20, "Total elapsed time: %s sec",
                        end_time - start_time)  # Prints total elapsed time of the process

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
        data_folder : str
            Path to the raw data folder

        Returns
        -------
        self.data_folder : str
            Path to the raw data folder

        """
        self.data_folder = data_folder
        if not os.path.exists(self.data_folder):
            logging.error("%s: This folder doesn't exist, please verify your data folder", data_folder)
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
            logging.error('%s: Cannot create results folder, please verify your data folder', folder)
        else:
            self.results_folder = os.path.join(folder, 'derivatives', 'automagic')
            #print(self.results_folder)
            return self.results_folder

    def save_project(self):
        pass

X = Project("Stupid Project", "C:/Users\saul__000\OneDrive\Escritorio\Johns Hopkins/NeuroData Design I\Project_Test_Folder", "something.edf")
A = X.preprocess_all_test()
B = X.interpolate_selected()
