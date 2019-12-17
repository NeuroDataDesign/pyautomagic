import os.path


class Subject:
    """
    SUBJECT is a class representing each subject in the dataFolder.
    A Subject corresponds to a folder, which contains one or more
    Blocks. A Block represents a raw file and it's associated
    preprocessed file, if any (See Block).
    """

    # Constructor
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.name = self.extract_name(data_folder)
        self.result_folder = self.result_path(data_folder)

    def update_addresses(self, new_data_path, new_project_path):
        """
        This method is to be called to update addresses
        in case the project is loaded from another operating system and may
        have a different path to the dataFolder or resultFolder. This can
        happen either because the data is on a server and the path to it is
        different on different systems, or simply if the project is loaded
        from a windows to a iOS or vice versa.
        Parameters
        ----------
        new_data_path : str
            updated path of the data folder
        new_project_path : str
            updated path of the project folder
        Returns
        -------
        None

        """

        self.data_folder = os.path.join(new_data_path, self.name)
        self.result_folder = os.path.join(new_project_path, self.name)

    def result_path(self, data_folder):
        """
        finds the result folder path for the corresponding subject data folder according to the BIDS folder hierarchy.
        Parameters
        ----------
        data_folder : str
            subject data folder
        Returns
        -------
        result : str
            corresponding result folder
        """
        parent, _ = os.path.split(data_folder)
        result = os.path.join(parent, "derivatives", "automagic", f"sub-{self.name}")
        return result

    def result_path(self, data_folder):
        """
        finds the result folder path for the corresponding subject data folder according to the BIDS folder hierarchy.
        Parameters
        ----------
        data_folder : str
            subject data folder

        Returns
        -------
        result : str
            corresponding result folder

        """
        parent, _ = os.path.split(data_folder)
        result = os.path.join(parent, "derivatives", "automagic", f"sub-{self.name}")
        return result

    @staticmethod
    def extract_name(address):
        """
        extract the name of the subject from subject data folder.
        Parameters
        ----------
        address : str
            path of the subject folder

        Returns
        -------
        name : str
            name of the subject
        """
        head, tail = os.path.split(address)
        name = tail or os.path.basename(head)

        if name.startswith("sub-"):
            name = name.replace("sub-", "")
        return name
