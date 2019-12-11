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

import numpy as np

# File containing all Pyautomagic constant values

# Constant Global Values

class ConstantGlobalValues:

    VERSION = '1.0'

    DEFAULT_KEYWORD = 'Default'

    NONE_KEYWORD = 'None'

    NEW_PROJECT = {'LIST_NAME': 'Create New Project', 'NAME': 'Type the name of your new project',
                   'DATA_FOLDER': 'Choose where your raw data is',
                   'FOLDER': 'Choose where you want the results to be saved'}

    LOAD_PROJECT = {'List_Name': 'Load and existing project'}

    RATINGS = {'Good': 'Good', 'Bad': 'Bad', 'OK': 'OK', 'Interpolate': 'Interpolate',
               'NotRated': 'Not Rated'}

    EXTENSIONS = {'mat': '.mat', 'text': '.txt .asc .csv', 'fif': '.fif', 'set': '.set', 'edf': '.edf'}

    PYAUTOMAGIC = 'pyautomagic'

    PREPROCESSING_FOLDER = 'preprocessing'


# Default Parameters


class DefaultParameters:

    FILTER_PARAMS = {'notch': {}, 'high': {}, 'low': {}}

    CRD_PARAMS = {}

    PREP_PARAMS = {}

    HIGH_VAR_PARAMS = {}

    INTERPOLATION_PARAMS = {'method': 'spherical'}

    RPCA_PARAMS = {}

    MARA_PARAMS = {'largeMap': 0, 'high': {'freq': 1.0, 'order': []}}

    ICLABEL_PARAMS = {}

    EOG_REGRESSION_PARAMS = {}

    CHANNEL_REDUCTION_PARAMS = {}

    DETRENDING_PARAMS = {}

    EEG_SYSTEM = {'name': 'Others', 'sys10_20': 0, 'locFile': '', 'refChan': {'idx': {}}, 'fileLocType': '',
                  'eogChans': {}, 'powerLineFreq': {}}

    SETTINGS = {'trackAllSteps': 0}

    PARAMS = {'line_frequencies': 50, 'filter_type': 'high', 'filt_freq': None, 'filter_length': 'auto', 'eog_regression': False, 'lam': -1, 'tol': 1e-7, 'max_iter': 1000}


# Pre processing Constants


class PreprocessingConstants:

    FILTER_CSTS = {'NOTCH_EU': 50, 'NOTHC_US': 60, 'NOTCH OTHER': {}, 'RUN MESSAGE': 'Perform Filtering...'}

    EEG_LAB_CSTS = {'ZIP': 'eeglab14_1_2b.zip'}

    CRD_CSTS = {'URL': 'http://sccn.ucsd.edu/eeglab/plugins/clean_rawdata0.32.zip', 'ZIP': 'clean_rawdata0.32.zip',
                'RUN MESSAGE': 'Finding Bad Channels...'}

    PREP_CSTS = {'URL': 'https://github.com/VisLab/EEG-Clean-Tools/archive/master.zip',
                 'ZIP': 'VisLab-EEG-Clean-Tools.zip'}

    RPCA_CSTS = {'URL': 'http://perception.csl.illinois.edu/matrix-rank/Files/inexact_alm_rpca.zip',
                 'ZIP': 'inexact_alm_rpca.zip', 'RUN_MESSAGE': 'Performing Robust PCA  (this may take a while...)'}

    IC_LABEL_CSTS = {'ZIP': 'ICLabel0.3.1.zip', 'RUN_MESSAGE': 'Performing ICLabel (this may take a while...)'}

    EOG_REGRESSION_CSTS = {'RUN_MESSAGE': 'Perform EOG Regression...'}

    GENERAL_CSTS = {'ORIGINAL_FILE': ' ', 'REDUCED_NAME': 'reduced'}

    EEG_SYSTEM_CSTS = {'sys10_20_file': 'standard-10-5-cap385.elp', 'EGI_NAME': 'EGI', 'OTHERS_NAME': 'Others'}

    SETTINGS_PREP = {'pathToSteps': '/allSteps'}


# Recommended Parameters


class RecommendedParameters:

    FILTER_PARAMS_REC = {'notch': {'freq': 50}, 'high': {'freq': 0.5, 'order': {}}, 'low': {'freq': 30, 'order': {}}}

    CRD_PARAMS_REC = {'ChannelCriterion': 0.85, 'LineNoiseCriterion': 4, 'BurstCriterion': 5, 'WindowCriterion': 0.25,
                      'Highpass': np.array([0.25, 0.75])}

    PREP_PARAMS_REC = {}

    HIGH_VAR_PARAMS_REC = {'sd': 25}

    INTERPOLATION_PARAMS_REC = {'method': 'spherical'}

    RPCA_PARAMS_REC = {'lambda': [], 'tol': 1e-7, 'maxIter': 1000}

    EOG_REGRESSION_PARAMS_REC = {}

    DETRENDING_PARAMS_REC = {}

    CHANNEL_REDUCTION_PARAMS_REC = {'tobeExcludedChans': []}

    EEG_SYSTEM_REC = {'name': 'Others', 'standard_1020': 0, 'locFile': '', 'refChan': {'idx': []}, 'fileLocType': '',
                      'eogChans': [], 'powerLineFreq': []}

    SETTINGS_REC = {'trackAllSteps': 0, 'pathToSteps': '/allSteps.mat'}


# Default Visualisation Parameters

class DefaultVisualizationParameters:

    COLOR_SCALE = 100

    DS_RATE = 2

    CALC_QUALITY_PARAMS = {'overallThresh': np.arange(20, 40, 5), 'timeThresh': np.arange(5, 25, 5),
                           'chanThresh': np.arange(5, 25, 5), 'avRef': 1}

    RATE_QUALITY_PARAMS = {'overallGoodCutoff': 0.1, 'overallBadCutoff': 0.2, 'timeGoodCutoff': 0.1,
                           'timeBadCutoff': 0.2, 'channelGoodCutoff': 0.15, 'channelBadCutoff': 0.3,
                           'BadChannelGoodCutoff': 0.15, 'BadChannelBadCutoff': 0.3,
                           'Qmeasure': {'THV', 'OHA', 'CHV', 'RBC'}}
