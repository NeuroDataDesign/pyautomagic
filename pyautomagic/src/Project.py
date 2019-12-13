import logging
import os

logger = logging.getLogger(__name__)

class Project():
    def __init__(self,root_path,config,params,sampling_rate,visualization_params,
                 quality_thresholds,rate_cutoffs,montage):
        self.name = os.path.basename(root_path)
        self.config = config
        self.params = params = {'line_freqs' : 50,\
                      'filter_type' : 'high', \
                      'filt_freq' : None, \
                      'filter_length' : 'auto', \
                      'eog_regression' : False, \
                      'lam' : -1, \
                      'tol' : 1e-7, \
                      'max_iter': 1000, \
                      'ref_chs': None,\
                      'eval_chs': None,\
                      'reref_chs': None, \
                      }
        self.sampling_rate = sampling_rate
        self.visualization_params = visualization_params
        self.quality_thresholds = quality_thresholds
        self.rate_cutoffs = rate_cutoffs
        self.montage =  montage

    def update_rating_list(self):
        return
