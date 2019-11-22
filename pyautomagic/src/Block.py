from pyautomagic.src.Subject import Subject

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
