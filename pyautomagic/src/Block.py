#from typing import List
import logging
#import numpy as np
import os
#import re
import json
#from pyautomagic.src.calcQuality import calcQuality
import mne
from mne_bids.utils import _parse_bids_filename, _write_json
from mne_bids.read import _read_raw
from pyautomagic.preprocess.preprocess import preprocess, interpolate
from pyautomagic.src.calcQuality import calcQuality
from pyautomagic.src.rateQuality import rateQuality
from matplotlib import pyplot as plt


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
        self = self.update_rating_from_file
        self.visualization_params = project.visualization_params
        
    
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
            result_path = os.path.join(self.root_path,'derivatives','automagic',f"sub-{params['sub']}")
        else:
            result_path = os.path.join(self.root_path,'derivatives','automagic',f"sub-{params['sub']}",f"ses-{params['ses']}")
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
        data = self.load_data
        preprocessed,fig_1,fig_2 = preprocess(data,self.params)
        quality_scores = calcQuality(preprocessed,self.final_bad_chans,self.project.quality_thresholds)
        automagic = preprocessed.pop('automagic')
        update_to_be_stored = {'rate':'not rated','is_manually_rated':False,
                               'to_be_interpolated':automagic['auto_bad_chans'],
                               'final_bad_chans':[],'is_interpolated':False,
                               'quality_scores':quality_scores,'commit':True}
        self.update_rating(update_to_be_stored)
        automagic.update({'to_be_interpolated':automagic.auto_bad_chans,
                          'final_bad_chans':self.final_bad_chans,
                          'version':self.project.config.version,
                          'quality_scores':self.quality_scores,
                          'quality_thresholds':self.project.quality_thresholds,
                          'rate':self.rate,
                          'is_manually_rated':self.is_manually_rated,
                          'times_commited':self.times_commited})
        results = {'preprocessed':preprocessed,'automagic':automagic}
        self.save_all_files(results,fig_1,fig_2)
        self.write_log(results)
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
        params = _parse_bids_filename(self.unique_name, verbose=False)
        if params['ses'] is None :
            data_path = os.path.join(self.root_path,f"sub-{params['sub']}",self.unique_name)
        else:
            data_path = os.path.join(self.root_path,f"sub-{params['sub']}",f"ses-{params['ses']}",self.unique_name)
        
        raw_filepath = data_path+self.file_ext
        _read_raw(raw_filepath)
        
    def update_rating(self,update):
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
        if 'quality_scores' in update:
            self.quality_scores = update.quality_scores
        if 'rate' in update:
            self.rate = update['rate']
            if not self.rate == 'interpolate' and not 'to_be_interpolated' in update:
                self.to_be_interpolated = []
        if 'is_manually_rated' in update:
            this_rate = rateQuality(self.quality_scores,self.project.rate_cutoffs)
            if update['is_manually_rated'] and not update['rate'] == this_rate:
                self.is_manually_rated = True
            elif not update['is_manually_rated']:
                self.is_manually_rated = False
        if 'to_be_interpolated' in update:
            self.to_be_interpolated = update['to_be_interpolated']
            if not update['to_be_interpolated'] == []:
                self.rate = 'interpolate'
        if 'final_bad_chans' in update:
            if update['final_bad_chans'] == []:
                self.final_bad_chans = update['final_bad_chans']
            else:
                self.final_bad_chans.extend(update['final_bad_chans'])
        if 'is_interpolated' in update:
            self.is_interpolated = update['is_interpolated']
        if 'commit' in update and update['commit'] == True:
            self.times_committed += 1
            
        self.project.update_rating_list(self)
    def save_all_files(self,results,fig1,fig2):
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
        main_result_file = results.info['automagic']
        result_filename = self.unique_name + '_results.json'
        result_file_overall = os.path.join(self.result_path,result_filename)
        _write_json(result_file_overall,main_result_file,overwrite=True,verbose = True)
        
        processed_filename = self.unique_name+'_raw.fif'
        processed_file_overall = os.path.join(self.result_path,processed_filename)
        results.save(processed_file_overall,overwrite=True)

        plt.figure(fig1.number)
        fig1_name = self.unique_name + '.png'
        fig1_name_overall = os.path.join(self.result_path,fig1_name)
        plt.savefig(fig1_name_overall,dpi=200)
        plt.figure(fig2.number)
        fig2_name = self.unique_name + '_orig.png'
        fig2_name_overall = os.path.join(self.result_path,fig2_name)
        plt.savefig(fig2_name_overall,dpi=100)
        
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
        logger.info(f'pyautomagic version {self.config[''version'']}')
        logger.info(f'Project:{self.project.name}, Subject:{self.subject.name}, File: {self.uniquename}')
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        # TODO: log more things from the preprocessing
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
        result_filename = self.unique_name + '_results.json'
        result_file_overall = os.path.join(self.result_path,result_filename)
        if os.path.isfile(result_file_overall):
            with open(result_file_overall) as json_file:
                automagic = json.load(json_file)
        processed_filename = self.unique_name+'_raw.fif'
        processed_file_overall = os.path.join(self.result_path,processed_filename)
        eeg = _read_raw(processed_file_overall)
        interpolate_chans = self.to_be_interpolated
        if interpolate_chans ==[]:
            raise(ValueError, 'The subject is rated to be interpolated but no channels chosen')
            return
        if self.params == [] or not 'interpolation_params' in self.params or self.params['interpolation_params'] == []:
            default_params = self.config['default_params']
            interpolation_params = default_params['interpolation_params']
        else:
            interpolation_params = self.params['interpolation_params']
        interpolated = interpolate(eeg,interpolate_chans,interpolation_params['method'])
        
        quality_scores = calcQuality(preprocessed,self.final_bad_chans,self.project.quality_thresholds)
        update_to_be_stored = {'rate':'not rated','is_manually_rated':False,
                               'to_be_interpolated':[],
                               'final_bad_chans':interpolate_chans,
                               'is_interpolated':True,
                               'quality_scores':quality_scores}
        self.update_rating(update_to_be_stored)
        automagic.update({'interpolation':{'channels':interpolate_chans,
                                           'params': interpolation_params},
                          'quality_scores':self.quality_scores,
                          'rate':self.rate})
        results = {'preprocessed':interpolated,'automagic':automagic}
        self.write_log(automagic)
        automagic.update({'to_be_interpolated':self.to_be_interpolated,
                          'rate':self.rate,
                          'auto_bad_chans':self.auto_bad_chans,
                          'quality_scores':self.quality_scores,
                          'rate':self.rate})
        # load up the preprocessed results file from results location
        # perform the interpolation (uses some EEGLab stuff I believe)
        # calcQuality
        # update block info, update results file info
        # save fils
        # write log

        