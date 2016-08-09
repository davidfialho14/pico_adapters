import os

import sys

from configs.base import BaseConfiguration, LoadError


class AethalometerConfiguration(BaseConfiguration):
    """
    Subclasses the Configuration class to adapt for the aethalometer
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
        a LoadError if not. It also checks if the store and backup directories
        exist and raises a load error if at least one of them does not exist.
        """
        for key, value in self._params.items():
            if value is None:
                raise LoadError("the configuration file is missing "
                                "the parameter '%s'" % key)

        store_dir = self.store_dir
        if not os.path.exists(store_dir):
            raise LoadError("the store directory '%s' does "
                            "not exist" % store_dir)

        backup_dir = self.backup_dir
        if not os.path.exists(backup_dir):
            raise LoadError("the backup directory '%s' does "
                            "not exist" % backup_dir)
