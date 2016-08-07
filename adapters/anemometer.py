"""Anemometer

Usage:
  ./anemometer <config_file>
  ./anemometer (-h | --help)

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
import os
import sys

from docopt import docopt

from anemometer_data_storer import AnemometerDataStorer
from anemometer_decoder import AnemometerDecoder
from configs.anemometer import AnemometerConfiguration
from data_receiver import DataReceiver
from logger import Logging


def main():
    args = docopt(__doc__)

    Logging.info("Started")

    config = AnemometerConfiguration(args['<config_file>'])
    config.load()

    # check in the beginning if the directories in the configuration file exist

    store_dir = config.store_dir
    if not os.path.exists(store_dir):
        print("the store directory '%s' does not exist" % store_dir)
        sys.exit(1)

    backup_dir = config.backup_dir
    if not os.path.exists(backup_dir):
        print("the backup directory '%s' does not exist" % backup_dir)
        sys.exit(1)

    receiver = DataReceiver((config.ip_address, config.port),
                            AnemometerDecoder)
    receiver.register_data_handler(AnemometerDataStorer(store_dir, backup_dir))

    try:
        receiver.receive_forever()
    except KeyboardInterrupt:
        # user pressed Ctrl-C to close the program
        Logging.info("Closing...")

    Logging.info("Closed")


if __name__ == '__main__':
    main()
