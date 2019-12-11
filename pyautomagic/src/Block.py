import os


class Block:

    def __init__(self, root_path, data_filename, project, subject):
        self.unique_name = os.path.splitext(data_filename)[0]
        self.data_folder = root_path
        self.project = project
        self.subject = subject
        self.is_interpolated = False
        self.quality_scores = {}
        self.rate = 'Interpolate'

    def preprocess(self):
        results = {'preprocessed': 'A' 'B' 'C', 'automagic': {'A1' : 'B1'}}
        return results
        pass

    def interpolate(self):
        pass
