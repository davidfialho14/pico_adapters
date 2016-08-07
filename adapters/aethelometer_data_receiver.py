import socket as sock
from time import sleep

from data_handler import DataHandler
from data_receiver import DataReceiver
from logger import Logging


class AethelometerDataReceiver(DataReceiver):
    """ Implements the decoding of an aethelometer data line. """

    def _decode(self, data) -> str:
        """ Aethelometer data lines just need to be converted to strings. """
        return data.decode('utf-8')
