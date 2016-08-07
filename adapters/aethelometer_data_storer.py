import os
import re
import shutil

from data_storer import DataStorer
from logger import Logging


class AethelometerDataStorer(DataStorer):
    """
    Stores data lines inside files with the name BCDDMMYY.CSV, where DD is
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

    date_pattern = re.compile('"(?P<day>\d+)-(?P<month>\w+)-(?P<year>\d+)"')

    month_to_int = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    }

    def store(self, data: str):
        """ Stores the data inside the configured directory. """
        match_result = self.date_pattern.match(data)

        if match_result:
            out_filename = "BC%s%02d%s.CSV" % \
                              (match_result.group('day'),
                               self.month_to_int[match_result.group('month')],
                               match_result.group('year'))

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

            Logging.info("stored new line in %s" % out_filename)
