class LoadError(Exception):
    """ Raised when an error occurs while loading the config file. """


class Configuration:
    """ Abstracts the access to the configuration file. """

    def __init__(self, config_file):
        self.config_file = config_file

        # stores the config parameters
        self._params = {
            'ip_address': None,
            'port': None,
            'store_dir': None,
            'backup_dir': None
        }

    def load(self):
        """
        Loads the configuration file. Raises LoadError if the config file
        is corrupted.
        """
        with open(self.config_file) as file:
            for i, line in enumerate(file):
                try:
                    line = line.rstrip('\n\r')
                    key, value = line.split(':')
                except ValueError:
                    raise LoadError("error in line %d" % i)

                if key not in self._params:
                    raise LoadError("parameter '%s' is invalid" % key)

                self._params[key] = value

        if None in self._params.values():
            raise LoadError("configuration file is missing one or more "
                            "parameters")

    @property
    def ip_address(self):
        return self._params['ip_address']

    @property
    def port(self):
        return self._params['port']

    @property
    def store_dir(self):
        return self._params['store_dir']

    @property
    def backup_dir(self):
        return self._params['backup_dir']
