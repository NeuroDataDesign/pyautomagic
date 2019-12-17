# File containing all Pyautomagic constant values

# Constant Global Values


class ConstantGlobalValues:

    VERSION = "1.0"

    DEFAULT_KEYWORD = "Default"

    NONE_KEYWORD = "None"

    NEW_PROJECT = {
        "LIST_NAME": "Create New Project",
        "NAME": "Type the name of your new project",
        "DATA_FOLDER": "Choose where your raw data is",
        "FOLDER": "Choose where you want the results to be saved",
    }

    LOAD_PROJECT = {"List_Name": "Load and existing project"}

    RATINGS = {
        "Good": "Good",
        "Bad": "Bad",
        "OK": "OK",
        "Interpolate": "interpolate",
        "NotRated": "Not Rated",
    }

    EXTENSIONS = {
        "mat": ".mat",
        "text": ".txt .asc .csv",
        "fif": ".fif",
        "set": ".set",
        "edf": ".edf",
    }

    PYAUTOMAGIC = "pyautomagic"

    PREPROCESSING_FOLDER = "preprocessing"


# Default Parameters


class DefaultParameters:

    FILTER_PARAMS = {"notch": {}, "high": {}, "low": {}}

    CRD_PARAMS = {}

    PREP_PARAMS = {}

    HIGH_VAR_PARAMS = {}

    INTERPOLATION_PARAMS = {"method": "spherical"}

    RPCA_PARAMS = {}

    MARA_PARAMS = {"largeMap": 0, "high": {"freq": 1.0, "order": []}}

    ICLABEL_PARAMS = {}

    EOG_REGRESSION_PARAMS = {}

    CHANNEL_REDUCTION_PARAMS = {}

    DETRENDING_PARAMS = {}

    EEG_SYSTEM = {
        "name": "Others",
        "sys10_20": 0,
        "locFile": "",
        "refChan": {"idx": {}},
        "fileLocType": "",
        "eogChans": {},
        "powerLineFreq": {},
    }

    SETTINGS = {"trackAllSteps": 0}


# Pre processing Constants


class PreprocessingConstants:

    FILTER_CSTS = {
        "NOTCH_EU": 50,
        "NOTHC_US": 60,
        "NOTCH OTHER": {},
        "RUN MESSAGE": "Perform Filtering...",
    }

    EOG_REGRESSION_CSTS = {"RUN_MESSAGE": "Perform EOG Regression..."}

    GENERAL_CSTS = {"ORIGINAL_FILE": " ", "REDUCED_NAME": "reduced"}

    EEG_SYSTEM_CSTS = {
        "sys10_20_file": "standard-10-5-cap385.elp",
        "EGI_NAME": "EGI",
        "OTHERS_NAME": "Others",
    }

    SETTINGS_PREP = {"pathToSteps": "/allSteps"}


# Recommended Parameters


class RecommendedParameters:

    FILTER_PARAMS_REC = {
        "notch": {"freq": 50},
        "high": {"freq": 0.5, "order": {}},
        "low": {"freq": 30, "order": {}},
    }

    CRD_PARAMS_REC = {
        "ChannelCriterion": 0.85,
        "LineNoiseCriterion": 4,
        "BurstCriterion": 5,
        "WindowCriterion": 0.25,
        "Highpass": [0.25, 0.75],
    }

    PREP_PARAMS_REC = {}

    HIGH_VAR_PARAMS_REC = {"sd": 25}

    INTERPOLATION_PARAMS_REC = {"method": "spherical"}

    RPCA_PARAMS_REC = {"lambda": [], "tol": 1e-7, "maxIter": 1000}

    EOG_REGRESSION_PARAMS_REC = {}

    DETRENDING_PARAMS_REC = {}

    CHANNEL_REDUCTION_PARAMS_REC = {"tobeExcludedChans": []}

    EEG_SYSTEM_REC = {
        "name": "Others",
        "standard_1020": 0,
        "locFile": "",
        "refChan": {"idx": []},
        "fileLocType": "",
        "eogChans": [],
        "powerLineFreq": [],
    }

    SETTINGS_REC = {"trackAllSteps": 0, "pathToSteps": "/allSteps.mat"}


# Default Visualisation Parameters


class DefaultVisualizationParameters:

    COLOR_SCALE = 100

    DS_RATE = 2

    CALC_QUALITY_PARAMS = {
        "overall_thresh": [20, 25, 30, 35],
        "time_thresh": [5, 10, 15, 20],
        "chan_thresh": [5, 10, 15, 20],
        "apply_common_avg": 1,
    }

    RATE_QUALITY_PARAMS = {
        "overall_Good_Cutoff": 0.1,
        "overall_Bad_Cutoff": 0.2,
        "time_Good_Cutoff": 0.1,
        "time_Bad_Cutoff": 0.2,
        "channel_Good_Cutoff": 0.15,
        "channel_Bad_Cutoff": 0.3,
        "bad_Channel_Good_Cutoff": 0.15,
        "bad_Channel_Bad_Cutoff": 0.3,
        "Q_measure": {"THV", "OHA", "CHV", "RBC"},
    }
