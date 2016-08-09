"""Anemometer

Usage:
  ./anemometer <config_file>
  ./anemometer (-h | --help)

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
import os
import signal
import sys

from docopt import docopt

from anemometer_data_storer import AnemometerDataStorer
from anemometer_decoder import AnemometerDecoder
from configs.anemometer import AnemometerConfiguration
from configs.base import LoadError
from data_receiver import DataReceiver
from logger import Logging


def raise_keyboard_interrupt(signum, frame):
    raise KeyboardInterrupt


def main():
    args = docopt(__doc__)

    try:
        config = AnemometerConfiguration(args['<config_file>'])
        config.load()
    except LoadError as error:
        print(str(error))
        sys.exit(1)

    # make terminate signals raise keyboard interrupts
    signal.signal(signal.SIGTERM, raise_keyboard_interrupt)

    receiver = DataReceiver((config.ip_address, config.port),
                            AnemometerDecoder)
    receiver.register_data_handler(AnemometerDataStorer(config.store_dir,
                                                        config.backup_dir))

    try:
        Logging.info("Started")
        receiver.receive_forever()
    except KeyboardInterrupt:
        # user pressed Ctrl-C to close the program
        Logging.info("Closing as requested by user...")
    except BaseException:
        Logging.exception("Program will closed due to unexpected error...")

    Logging.info("Closed")


if __name__ == '__main__':
    main()
