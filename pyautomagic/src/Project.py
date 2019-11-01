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
logger = logging.getLogger(__name__)

#class Project:

def __init__(self, name: str, data_folder: str, results_folder: str, file_extension: str, preprocess_parameters: dict, visualisation_parameters: dict):
    self.name = name
    self.data_folder = data_folder
    self.results_folder = results_folder
    self.file_extension = file_extension
    self.preprocess_parameters = preprocess_parameters
    self.visualisation_parameters = visualisation_parameters


def Set_Name():
    name = input("Project Name: ")  # Asks the user to type the project name
    return name


def Set_data_folder():
    data_folder = input("Please enter the path to the data folder: ")  # Asks the user to type the data folder path
    return data_folder


def Set_results_folder():
    results_folder = input("Please enter the path where you want your results: ")  # Asks the user to type the results folder path
    return results_folder


def Preprocess_All(self):
    if not (os.path.isdir(self.data_folder)):
        logger.error("No directory exists, please specify the correct data directory")  # Displays error mesagge if no data directory found
    else:
        logger.log(20, "----- START PREPROCESSING -----")
        start_time = time.process_time()  # Calculates start time = CPU time
        for i in range(1, len(self.blockList)):
            uniqueName = self.blockList[i]
            block = self.blockMap(uniqueName)
            block.updateAddresses(self.data_folder, self.results_folder, self.params.EEGSystem.locFile)
            # subjectName = block.subject.name ----- subject name? how to access it?

            print("Processing file ", block.uniqueName, "file", i, "out of", (len(self.blockList)) )

            # if not (os.path.exists(self.results_folder)):
            #   bla bla bla ---- how to verify if the results folder for subjectName exists?

            [EEG] = block.preprocess()  # Call preprocess function to preprocess EEG data

            if len(EEG) == 0:
                logger.error("ERROR: EEG DATA NOT FOUND")

            self.saveProject()  # Save Project Function

        end_time = start_time - time.process_time()  # Calculates end time
        logger.log(20, "----- PREPROCESSING FINISHED -----")
        logger.info("Total elapsed time: ", end_time)  # Prints total elapsed time of the process


def Interpolate_Selected(self):

    if len(self.interpolateList) == 0:
        logger.error("Interpolate subjects list is empty, please rate first")

    else:
        logger.log(20, "----- START INTERPOLATION -----")
        start_time = time.process_time()  # Calculates start time = CPU time
        for i in range(1, len(self.interpolateList)):
            uniqueName = self.blockList[i]
            block = self.blockMap(uniqueName)
            block.updateAddresses(self.data_folder, self.results_folder, self.params.EEGSystem.locFile)

            print("Processing file ", block.uniqueName, "file", i, "out of", (len(self.interpolateList)))

            block.interpolate()

            self.alreadyInterpolated = [self.alreadyInterpolated, i]

            self.saveProject()

        end_time = start_time - time.process_time()  # Calculates end time
        logger.log(20, "----- INTERPOLATION FINISHED -----")
        logger.info("Total elapsed time: ", end_time)  # Prints total elapsed time of the process
