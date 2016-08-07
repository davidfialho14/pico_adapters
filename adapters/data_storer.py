from data_handler import DataHandler


class DataStorer(DataHandler):
    """
    Data storer is an implementation of a data handler which stores the data
    according to implementation.
    """

    def on_new_data(self, data):
        """ Calls the store method. """
        self.store(data)

    def store(self, data: str):
        """ Stores the data line according to the implementation. """
        pass
