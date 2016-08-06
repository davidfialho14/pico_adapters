from aethelometer.data_handler import DataHandler


class DataStorer(DataHandler):
    """
    Data storer is an implementation of a data handler which stores the data
    inside a directory and in specific files.
    """

    def __init__(self, data_dir):
        """
        :param data_dir: directory where to store the data.
        """
        self.data_dir = data_dir

    def on_new_data(self, data):
        """ Calls the store method. """
        self.store(data)

    def store(self, data):
        """ Stores the data inside the configured directory. """
        pass
