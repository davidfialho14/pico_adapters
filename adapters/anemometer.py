"""Anemometer

Usage:
  ./anemometer <config_file>
  ./anemometer (-h | --help)

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt

from anemometer_data_storer import AnemometerDataStorer
from anemometer_decoder import AnemometerDecoder
from app import Application
from configs.anemometer import AnemometerConfiguration


def main():
    app = Application(args=docopt(__doc__))
    config = app.load_config(AnemometerConfiguration)

    app.run(decoder=AnemometerDecoder,
            data_handlers=(AnemometerDataStorer(config.store_dir,
                                                config.backup_dir),))

if __name__ == '__main__':
    main()
