"""AethelometerAdapter

Usage:
  aethelometer.py <config_file>
  aethelometer.py (-h | --help)

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt

from aethelometer.configuration import Configuration
from aethelometer.data_receiver import DataReceiver
from aethelometer.data_storer import DataStorer


def main():
    args = docopt(__doc__)

    config = Configuration(args['<config_file>'])
    config.load()

    receiver = DataReceiver((config.ip_address, config.port))
    receiver.register_data_handler(DataStorer(config.store_dir))

    try:
        receiver.receive_forever()
    except KeyboardInterrupt:
        # user pressed Ctrl-C to close the program
        print("Closing...")

    print("Closed")


if __name__ == '__main__':
    main()
