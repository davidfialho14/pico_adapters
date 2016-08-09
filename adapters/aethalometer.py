"""Aethalometer

Usage:
  ./aethalometer <config_file>
  ./aethalometer (-h | --help)

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt

from aethalometer_data_storer import AethalometerDataStorer
from aethalometer_decoder import AethalometerDecoder
from app import Application
from configs.aethalometer import AethalometerConfiguration


def main():
    app = Application(args=docopt(__doc__))
    config = app.load_config(AethalometerConfiguration)

    app.run(decoder=AethalometerDecoder,
            data_handlers=(AethalometerDataStorer(config.store_dir,
                                                  config.backup_dir),))

if __name__ == '__main__':
    main()
