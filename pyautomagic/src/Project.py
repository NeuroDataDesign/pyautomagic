import logging
import os

logger = logging.getLogger(__name__)

class Project():
    def __init__(self,root_path,config,params,sampling_rate,visualization_params,
                 quality_thresholds,rate_cutoffs):
        self.name = os.path.basename(root_path)
        self.config = config
        self.params = params
        self.sampling_rate = sampling_rate
        self.visualization_params = visualization_params
        self.quality_thresholds = quality_thresholds
        self.rate_cutoffs = rate_cutoffs
        
    def update_rating_list(self):
        return