"""DataTaker

Usage:
  ./datataker <config_file>
  ./datataker (-h | --help)

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt

from datataker_connection_handler import DataTakerConnectionHandler
from datataker_data_storer import DataTakerDataStorer
from datataker_decoder import DataTakerDecoder
from app import Application
from configs.datataker import DataTakerConfiguration


def main():
    app = Application(args=docopt(__doc__))
    config = app.load_config(DataTakerConfiguration)

    app.run(decoder=DataTakerDecoder,
            data_handlers=(DataTakerDataStorer(config.store_dir,
                                               config.backup_dir),),
            connection_handlers=((DataTakerConnectionHandler(config.cmd_file)),))

if __name__ == '__main__':
    main()
