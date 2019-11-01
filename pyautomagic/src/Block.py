#from typing import List
import logging
#import numpy as np
import os
#import re
import json
#from pyautomagic.src.calcQuality import calcQuality

from mne_bids.utils import _parse_bids_filename
from mne_bids.read import _read_raw

logger = logging.getLogger(__name__)

class Block():
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
    times_commited : int
        used to track how many changes were made to the evaluation of the data

    """
    def __init__(self,root_path,data_filename,project,subject):
        self.project = project
        self.subject = subject
        self.unique_name = os.path.splitext(data_filename)[0]
        self.file_ext = os.path.splitext(data_filename)[1]
        self.params = project.params
        self.sampling_rate = project.sampling_rate
        self.root_path = root_path
        self.result_path = self.find_result_path
        
    
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
        result_filename = self.unique_name + '_results.json'
        result_file_overall = os.path.join(self.result_path,result_filename)
        if os.path.isfile(result_file_overall):
            with open(result_file_overall) as json_file:
                block = json.load(json_file)
            saved_params = block['params']
            if not saved_params==self.params:
                raise ValueError('Parameters of results file do not match this project. Can not merge.')
            if block.is_interpolated or block.is_rated:
                self.rate = block.rate
                self.to_be_interpolated = block.to_be_interpolated
                self.is_interpolated = block.is_interpolated
                self.auto_bad_chans = block.auto_bad_chans
                self.final_bad_chans = block.final_bad_chans
                self.quality_scores = block.quality_scores
                self.times_commited = block.times_commited
            else: 
                self.rate = 'not rated'
                self.to_be_interpolated = []
                self.is_interpolated = False
                self.auto_bad_chans = []
                self.final_bad_chans = []
                self.quality_scores = None
                self.times_commited = 0
                
        
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
        if params['ses'] is None :
            result_path = op.join(self.root_path,'derivatives','automagic',f"sub-{params['sub']}")
        else:
            result_path = op.join(self.root_path,'derivatives','automagic',f"sub-{params['sub']}",f"ses-{params['ses']}")
        return result_path

    def preprocess(self):
        """
        Preprocesses the raw data associated with this block
        
        Parameters
        ----------
        none
        
        Returns
        -------
        preprocessed: dict
            dictionary containing all the new updates to the block and the preprocessed array
            
        """
        data = load_data(self)
        # do some parameter checks
        # use externally written function to preprocess
        # calcQuality
        # update self.Quality
        # store a bunch of stuff into an automagic object for results file
        # save files
        # write log
    def load_data(self):
        """
        Load raw data from BIDS folder
        
        Allowing for a number of extensions, loads file
        
        Parameters
        ----------
        none
        
        Yields
        ------
        raw MNE object
        
        """
        raw_filepath = self.unique_name+self.file_ext
        _read_raw(raw_filepath)
        
    def update_rating(self,update):
        """
        Takes update about ratings and stores in object
        
        From project level object, get an update on rating info.
        
        Parameters
        ----------
        update : dict
            dictionary of updates
        
        Yields
        ------
        raw MNE object
        """
        # update can have many fields, go through and see what they are and update the block accordingly

    def save_all_files(self,fig1,fig2):
        """
        Save results dictionary and figures to results path
        
        Parameters
        ----------
        fig1:
            Figure of ??
        
        fig2:
            Figure of ??
        
        Returns
        -------
        none
        
        """
        # save the processed stuff and figures into results path
        # dict_to_save = vars(self)
        # _write_json(result_name,dict_to_save,overwrite=True,verbose = True) - obj save
        # save figs, store processed eeg - could add to above dict
    def write_log(self,updates):
        """
        Writes a log for all of the updates its making/actions performed
        Parameters
        ----------
        updates: dict
        
        Returns
        -------
        log object???
        
        """
        
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
        # load up the preprocessed results file from results location
        # perform the interpolation (uses some EEGLab stuff I believe)
        # calcQuality
        # update block info, update results file info
        # save fils
        # write log
    def update_fields(self,new_rating,is_rated,is_interpolated):
        self.rating = new_rating
        self.is_rated = is_rated
        self.is_interpolated = is_interpolated
            
    def create_results_file(self):
        """
        Takes object information needed to be saved and creates dictionary
        
        Parameters
        ----------
        none
        
        Returns
        -------
        results: dict
            dictionary containing all of the relevant info needed to be saved
        
        """
        # get the preprocessed file and do updates from Block info
        # write log