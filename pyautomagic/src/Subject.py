import ntpath


class Subject:

    def __init__(self, data_folder, result_folder):
        self.result_folder = result_folder
        self.data_folder = data_folder
        self.name = self.extract_name(data_folder)

    def update_addresses(self, new_data_path, new_project_path):
        """
            This method is to be called to update addresses
            in case the project is loaded from another operating system and may
            have a different path to the dataFolder or resultFolder. This can
            happen either because the data is on a server and the path to it is
            different on different systems, or simply if the project is loaded
            from a windows to a iOS or vice versa.
        """

        self.data_folder = ntpath.join(new_data_path, self.name)
        self.result_folder = ntpath.join(new_project_path, self.name)

    @staticmethod
    def extract_name(address):
        head, tail = ntpath.split(address)
        return tail or ntpath.basename(head)
