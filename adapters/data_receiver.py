import socket as sock
from time import sleep

from data_handler import DataHandler
from logger import Logging


class DataReceiver:
    """
    The Data Receiver is responsible for the communication with the
    sender. It can be associated with one or more data handlers. When it
    receives a new chunk of data calls the data handlers' on_new_data() method.
    """

    def __init__(self, sender_address):
        self._sender_address = sender_address
        self._data_handlers = []

        # stores the data that may have been transferred during a receive call
        # and did not belong to the current line
        self._cached_data = ""

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

        while True:  # allow reconnecting on error
            try:
                Logging.debug("Trying to connect to %s:%s..." %
                              (self._sender_address[0],
                               self._sender_address[1]))
                with sock.create_connection(self._sender_address,
                                            timeout=30) as connection:
                    Logging.debug("Connected successfully")

                    while True:
                        Logging.info("Waiting for data...")
                        data = self._receive(connection)
                        Logging.info("Received data")

                        for handler in self._data_handlers:
                            handler.on_new_data(data)

            except (ConnectionAbortedError, sock.timeout):
                Logging.warning("connection timed out")
            except (sock.herror, sock.gaierror):
                Logging.error("the address of the sender is not valid")
                break  # leave the function
            except (ConnectionRefusedError, sock.error):
                Logging.warning("can not reach the sender")

            # retry in connecting in 10 seconds
            Logging.debug("connection failed: will try to connect in 10 seconds")
            sleep(10)

    def _receive(self, sender_connection) -> str:
        """
        Blocks until a new chunk of data is received or the connection with the
        sender fails. Before calling this method there must be already a valid
        connection with the sender. Raises a socket.timeout if it does not
        receive any message from the server in 6 minutes or if after receiving
        data it does not receive more after 1 minute.
        :param sender_connection: socket connection with the sender.
        :return: data received.
        """
        # set a receive timeout of 6 minutes
        sender_connection.settimeout(6 * 60)

        # get the data cached in the previous receive call
        data = self._cached_data
        self._cached_data = ""  # ensure the cached data is cleared

        while True:
            # the verification of end of data must be the first step of the loop
            # this is because the cached data ma contain a complete line already

            end_index = data.find("\r\n")
            if end_index != -1:
                # reached the end of the data

                # cache extra data
                self._cached_data = data[end_index + 2:]

                # exclude extra data from the returned data
                data = data[0:end_index]
                break

            buffer = sender_connection.recv(512)

            if not buffer:
                raise ConnectionAbortedError("connection with sender was "
                                             "correctly closed")

            if not data:  # check if this is the first data chunk
                # after receiving data chunk set a timeout of 1 minute
                # this timeout prevents errors due to the server not finishing
                # the transmission
                sender_connection.settimeout(1 * 60)

            data += buffer.decode('utf-8')

        return data
