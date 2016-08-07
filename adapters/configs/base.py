import logging


class LoadError(Exception):
    """ Raised when an error occurs while loading the config file. """


class BaseConfiguration:
    """
    Abstracts the access to the configuration file. This is the base class
    to access configuration files. It accepts any parameter key and value.
    The responsibility to check the validity of parameters and values is given
    to the specific implementations.
    """

    def __init__(self, config_file):
        self.config_file = config_file

    def load(self):
        """
        Loads the configuration file. Raises LoadError if the config file
        is corrupted.
        """
        log_file = None  # will store the loaded path to the log file

        with open(self.config_file) as file:
            for i, line in enumerate(file):
                try:
                    line = line.rstrip('\n\r')
                    key, value = line.split(':')
                except ValueError:
                    raise LoadError("error in line %d" % i)

                if key == 'log':
                    log_file = value
                    continue

                self._add_param(key, value)

        self.__init_log(log_file)
        self._finished_loading()

    def _add_param(self, param_key, param_value):
        """
        Adds a new parameter to the list of loaded parameters. This must be
        implemented by the configuration subclasses. If the parameter key or
        value are not valid it must raise a LoadError.
        """
        pass

    def _finished_loading(self):
        """
        Called in the end of the load() method, once the loading of the
        configuration file finishes. Subclasses should implement this method
        accordingly if they want to take any action after loading. May raise
        a LoadError if the implementation detects a loading error at this point.
        """
        pass

    def __init_log(self, log_file):
        """
        Initiates the log file. If log_file is None the logs will be printed
        to the stdout.
        """
        logging.basicConfig(filename=log_file, level=logging.DEBUG,
                            format='%(asctime)s:%(levelname)s:%(message)s')
