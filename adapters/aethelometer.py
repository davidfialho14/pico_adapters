"""Aethelometer

Usage:
  ./aethelometer <config_file>
  ./aethelometer (-h | --help)

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
import os
import sys

from docopt import docopt

from aethelometer_data_storer import AethelometerDataStorer
from aethelometer_decoder import AethelometerDecoder
from configs.aethelometer import AethelometerConfiguration
from data_receiver import DataReceiver
from logger import Logging


def main():
    args = docopt(__doc__)

    config = AethelometerConfiguration(args['<config_file>'])
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
                            AethelometerDecoder)
    receiver.register_data_handler(AethelometerDataStorer(store_dir, backup_dir))

    try:
        Logging.info("Started")
        receiver.receive_forever()
    except KeyboardInterrupt:
        # user pressed Ctrl-C to close the program
        Logging.info("Closing...")

    Logging.info("Closed")


if __name__ == '__main__':
    main()
