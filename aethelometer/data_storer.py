import os
import re

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

            with open(out_filepath, "a") as out_file:
                out_file.write(data)
                out_file.write('\n')

            print("stored new line in %s" % out_filename)
