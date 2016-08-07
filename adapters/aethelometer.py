"""Aethelometer

Usage:
  aethelometer.py <config_file>
  aethelometer.py (-h | --help)

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
import os
import sys

from aethelometer.configuration import Configuration
from aethelometer.data_storer import DataStorer
from docopt import docopt

from adapters.data_receiver import DataReceiver


def main():
    args = docopt(__doc__)

    config = Configuration(args['<config_file>'])
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

    receiver = DataReceiver((config.ip_address, config.port))
    receiver.register_data_handler(DataStorer(store_dir, backup_dir))

    try:
        receiver.receive_forever()
    except KeyboardInterrupt:
        # user pressed Ctrl-C to close the program
        print("Closing...")

    print("Closed")


if __name__ == '__main__':
    main()
