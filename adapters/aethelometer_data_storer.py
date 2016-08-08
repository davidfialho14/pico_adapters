import re

from data_storer import DataStorer


class AethelometerDataStorer(DataStorer):
    """
    Stores data lines inside files with the name BCYYMMDD.CSV, where DD is
    the day of the data line, MM is the month of the line, and YY is the year.
    The files are stored in the store_dir and moved to the backup_dir once
    a new file is created.
    """

    date_pattern = re.compile('"(?P<day>\d+)-(?P<month>\w+)-(?P<year>\d+)"')

    month_to_int = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    }

    def _generate_filename(self, data: str, current_datetime) -> str:
        """ Generates filename with the format BCyymmdd.CSV"""
        match_result = self.date_pattern.match(data)

        if match_result:
            # use datetime from the data line
            return "BC%s%02d%s.CSV" % \
                   (match_result.group('year'),
                    self.month_to_int[match_result.group('month')],
                    match_result.group('day'))
        else:
            # use current datetime
            return current_datetime.strftime("BC%y%m%d.CSV")
