import socket
from contextlib import suppress
from datetime import datetime

from connection_handler import ConnectionHandler


class DataTakerConnectionHandler(ConnectionHandler):
    """
    Performs the necessary steps after the connections to configure the device.
    """

    def __init__(self, cmd_file):
        self._cmd_file = cmd_file

    def on_new_connection(self, data_receiver, connection, sender_address):
        """
        Sends the commands in the cmd_file to the device. Before sending the
        commands in the cmd_file sends the Time command.
        """
        # before sending commands always open the file to ensure it exists
        # before sending commands

        with suppress(FileNotFoundError):
            with open(self._cmd_file) as cmd_file:
                time_cmd = datetime.now().strftime("T=%H:%M:%S")
                self._deploy_cmd(data_receiver, connection, time_cmd)

                date_cmd = datetime.now().strftime("D=%d/%m/%Y")
                self._deploy_cmd(data_receiver, connection, date_cmd)

                for cmd in cmd_file:
                    self._deploy_cmd(data_receiver, connection,
                                     cmd.replace("\n", ""))

    def _deploy_cmd(self, data_receiver, connection, cmd):
        """
        After sending the command it waits 1 second for answers and
        ignores them.
        """
        try:
            self._send_cmd(connection, cmd)

            while True:
                if cmd == "RESET":
                    # handle the special case of the RESET command
                    # ignore everything until receiving the done response
                    # then ignore an extra empty line
                    answer = b''
                    while answer != b'Initializing...Done.':
                        self._receive_and_log(data_receiver, connection)
                    self._receive_and_log(data_receiver, connection)
                    break
                else:
                    self._receive_and_log(data_receiver, connection)

        except socket.timeout:
            pass
