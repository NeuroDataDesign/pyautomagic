import os
from pyautomagic.src.Project import Project


class Block:

    def __init__(self, root_path, data_filename, Project, Subject):
        self.unique_name = os.path.splitext(data_filename)[0]
        self.data_folder = root_path
        self.project = Project
        self.subject = Subject('name', '')
        self.is_interpolated = False
        self.quality_scores = {}

    def preprocess(self):
        results = {'preprocessed': 'A' 'B' 'C'}
        return results
        pass

    def interpolate(self):
        pass
