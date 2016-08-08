from configs.aethelometer import AethelometerConfiguration


class DataTakerConfiguration(AethelometerConfiguration):
    """
    Extends the aethelometer configuration by adding support for a cmd_file
    parameter.
    """

    def __init__(self, config_file):
        super().__init__(config_file)

        # include extra config param for the command file
        self._params['cmd_file'] = None

    @property
    def cmd_file(self):
        return self._params['cmd_file']
