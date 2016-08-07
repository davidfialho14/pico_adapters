from adapters.configs.base import BaseConfiguration, LoadError


class AethelometerConfiguration(BaseConfiguration):
    """
    Subclasses the Configuration class to adapt for the aethelometer
    configurations.
    """
    def __init__(self, config_file):
        super().__init__(config_file)

        # stores the config parameters
        self._params = {
            'ip_address': None,
            'port': None,
            'store_dir': None,
            'backup_dir': None
        }

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

    def _add_param(self, param_key, param_value):
        if param_key not in self._params:
            raise LoadError("parameter '%s' is invalid" % param_key)

        self._params[param_key] = param_value

    def _finished_loading(self):
        """
        Checks if all the necessary parameters were loaded. It raises
        a LoadError if not.
        """
        if None in self._params.values():
            raise LoadError("configuration file is missing one or more "
                            "parameters")
