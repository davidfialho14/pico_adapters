from data_storer import DataStorer


class AnemometerDataStorer(DataStorer):
    """
    Stores data lines inside files with the name 3DYYMMDD.CSV, where DD is
    the day of the data line, MM is the month of the line, and YY is the year.
    The files are stored in the store_dir and moved to the backup_dir once
    a new file is created.
    """

    def _adjust_data(self, data: str, current_datetime) -> str:
        """ Adds the date and time to the data line. """
        return current_datetime.strftime("%d-%m-%Y,%H:%M:%S,") + data

    def _generate_filename(self, data: str, current_datetime) -> str:
        """ Generates filename with the format 3Dyymmdd.CSV"""
        return current_datetime.strftime("3D%y%m%d.CSV")
