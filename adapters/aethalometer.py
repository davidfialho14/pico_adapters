"""Aethalometer

Usage:
  ./aethalometer <config_file>
  ./aethalometer (-h | --help)

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
import os
import signal
import sys

from docopt import docopt

from aethalometer_data_storer import AethalometerDataStorer
from aethalometer_decoder import AethalometerDecoder
from configs.aethalometer import AethalometerConfiguration
from configs.base import LoadError
from data_receiver import DataReceiver
from logger import Logging


def raise_keyboard_interrupt(signum, frame):
    raise KeyboardInterrupt


def main():
    args = docopt(__doc__)

    try:
        config = AethalometerConfiguration(args['<config_file>'])
        config.load()
    except LoadError as error:
        print(str(error))
        sys.exit(1)

    # make terminate signals raise keyboard interrupts
    signal.signal(signal.SIGTERM, raise_keyboard_interrupt)

    receiver = DataReceiver((config.ip_address, config.port),
                            AethalometerDecoder)
    receiver.register_data_handler(AethalometerDataStorer(config.store_dir,
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
