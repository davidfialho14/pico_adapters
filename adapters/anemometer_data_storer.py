import os
import shutil
from datetime import datetime

from data_storer import DataStorer
from logger import Logging


class AnemometerDataStorer(DataStorer):
    """
    Stores data lines inside files with the name 3DDDMMYY.CSV, where DD is
    the day of the data line, MM is the month of the line, and YY is the year.
    The files are stored in the store_dir and moved to the backup_dir once
    a new file is created.
    """

    def __init__(self, data_dir, backup_dir):
        """
        :param data_dir: directory where to store the data.
        """
        self.data_dir = data_dir
        self.backup_dir = backup_dir

    def store(self, data: str):
        """ Stores the data inside the configured directory. """
        current_datetime = datetime.now()

        # include the data time in the data line
        data = current_datetime.strftime("%d-%m-%Y,%H:%M:%S,") + data

        # filename has the format 3Dddmmyy.CSV
        out_filename = "3D" + current_datetime.strftime("%d%m%y") + ".CSV"
        out_filepath = os.path.join(self.data_dir, out_filename)

        if not os.path.exists(out_filepath):
            # new file will be created
            # move all current files inside the store dir to the backup dir
            for filename in os.listdir(self.data_dir):
                shutil.move(src=os.path.join(self.data_dir, filename),
                            dst=os.path.join(self.backup_dir, filename))
                Logging.info("moved file %s to the backup "
                             "directory" % filename)

        with open(out_filepath, "a") as out_file:
            out_file.write(data)
            out_file.write('\n')
