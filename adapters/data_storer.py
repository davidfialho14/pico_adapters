import os

import shutil
from datetime import datetime

from data_handler import DataHandler
from logger import Logging


class DataStorer(DataHandler):
    """
    Data storer is an implementation of a data handler which stores the data
    according in a data directory and may move data to a backup directory
    at a certain moment depending on the implementation.
    """

    def __init__(self, data_dir, backup_dir=None):
        """
        :param data_dir: directory where to store the data.
        """
        self.data_dir = data_dir
        self.backup_dir = backup_dir

    def on_new_data(self, data):
        """ Calls the store method. """
        self.store(data)

    def store(self, data: str):
        """ Stores the data line according to the implementation. """
        if not data:
            # ignore empty message
            return

        # the datetime passed to teh adjust_data() and generate_filename()
        # methods must be the same to avoid incoherency
        current_datetime = datetime.now()
        data = self._adjust_data(data, current_datetime)

        out_filename = self._generate_filename(data, current_datetime)
        out_filepath = os.path.join(self.data_dir, out_filename)

        # this must be called before dumping the data to the file
        self._backup_prev_files(out_filepath)

        with open(out_filepath, "a") as out_file:
            out_file.write(data)
            out_file.write('\n')

        Logging.info("stored new line in %s" % out_filename)

    def _adjust_data(self, data: str, current_datetime) -> str:
        """
        Invoked after the store method is called. By default it returns
        the received data, ut it should be overridden if any alteration
        to the data is needed before saving.
        """
        return data

    def _generate_filename(self, data: str, current_datetime) -> str:
        """
        Generates the filename according to the implementation.
        It takes the data line as it was received in the store() method.
        """
        pass

    def _backup_prev_files(self, current_filepath):
        """
        Moves the previous files to the backup directory. If the backup
        directory was not specified in the initializer it does nothing.
        """
        if self.backup_dir and not os.path.exists(current_filepath):
            # new file will be created
            # move all current files inside the store dir to the backup dir
            for filename in os.listdir(self.data_dir):
                shutil.move(src=os.path.join(self.data_dir, filename),
                            dst=os.path.join(self.backup_dir, filename))
                Logging.info("moved file %s to the backup "
                             "directory" % filename)
