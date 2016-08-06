import socket as sock

from aethelometer.data_handler import DataHandler


class DataReceiver:
    """
    The Data Receiver is responsible for the communication with the
    aethelometer. It can be associated with one or more data handlers. When it
    receives a new chunk of data calls the data handlers' on_new_data() method.
    """

    def __init__(self, sender_address):
        self._sender_address = sender_address
        self._data_handlers = []

    def register_data_handler(self, data_handler: DataHandler):
        """
        Registers a new data handler in the receiver.
        :param data_handler: new data handler to register.
        """
        self._data_handlers.append(data_handler)

    def remove_data_handler(self, data_handler: DataHandler):
        """
        Removes a data handler from the registered handlers.
        :param data_handler: data handler to be removed.
        """
        self._data_handlers.remove(data_handler)

    def receive_forever(self):
        """
        Puts the receiver in receiving mode forever. In this mode the receiver
        blocks until new data is received from the sender. Every time a new
        chunk of data is received it calls the registered handlers'
        on_new_data() method.
        """
        pass

    def _receive(self, sender_connection) -> str:
        """
        Blocks until a new chunk of data is received or the connection with the
        sender fails. Before calling this method there must be already a valid
        connection with the sender.
        :param sender_connection: socket connection with the sender.
        :return: data received.
        """
        pass
