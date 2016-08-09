import signal

import sys

from configs.base import LoadError
from data_receiver import DataReceiver
from logger import Logging


def raise_keyboard_interrupt(signum, frame):
    """ Handler for the Terminate signal. Raises a KeyboardException. """
    raise KeyboardInterrupt


class Application:
    """ Base class for an application"""

    def __init__(self, args):
        """ The args provided must use the format outputted by docopt. """
        self._args = args
        self._config = None

    def load_config(self, configuration):
        """
        Loads the configuration file using the provided configuration class.
        This method must be called before run().

        :param configuration: configuration class to be used.
        :return: loaded configuration object.
        """
        try:
            self._config = configuration(self._args['<config_file>'])
            self._config.load()
        except LoadError as error:
            print(str(error))
            sys.exit(1)

        return self._config

    def run(self, decoder, data_handlers, connection_handlers):
        """
        Runs the application after loading the configuration.
        If this method is called before loading the configuration a ValueError
        is raised.

        :param decoder: decoder to be used
        :param data_handlers: iterable with all the data handlers to register
                              with the data receiver.
        :param connection_handlers: iterable with all the connection handlers to
                                    register with the data receiver.
        """
        if not self._config:
            raise ValueError("can not run before loading the configuration")

        # make terminate signals raise keyboard interrupts
        signal.signal(signal.SIGTERM, raise_keyboard_interrupt)

        receiver = DataReceiver((self._config.ip_address, self._config.port),
                                decoder)

        # register all data handlers
        for handler in data_handlers:
            receiver.register_data_handler(handler)

        # register all connection handlers
        for handler in connection_handlers:
            receiver.register_connection_handler(handler)

        try:
            Logging.info("Started")
            receiver.receive_forever()
        except KeyboardInterrupt:
            # user pressed Ctrl-C to close the program
            Logging.info("Closing as requested by user...")
        except BaseException:
            Logging.exception("Program will closed due to unexpected error...")

        Logging.info("Closed")




