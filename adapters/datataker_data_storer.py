import re

from data_storer import DataStorer


class DataTakerDataStorer(DataStorer):
    """
    Stores data lines inside files with the name DKYYMMDD.CSV, where DD is
    the day of the data line, MM is the month of the line, and YY is the year.
    The files are stored in the store_dir and moved to the backup_dir once
    a new file is created.
    """

    date_pattern = re.compile('"(?P<day>\d+)/(?P<month>\d+)/(?P<year>\d+)"')

    def _generate_filename(self, data: str, current_datetime) -> str:
        """ Generates filename with the format DKYYMMDD.CSV"""
        match_result = self.date_pattern.match(data)

        if match_result:
            # use datetime from the data line
            return "DK%02d%s%s.CSV" % \
                   (int(match_result.group('year')) % 100,
                    match_result.group('month'),
                    match_result.group('day'))
        else:
            # use current datetime
            return current_datetime.strftime("DK%y%m%d.CSV")
