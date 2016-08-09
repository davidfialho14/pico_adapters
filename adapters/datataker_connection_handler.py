import socket
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
        time_cmd = datetime.now().strftime("T=%H:%M:%S")
        self._send_cmd(connection, time_cmd)

        date_cmd = datetime.now().strftime("D=%d/%m/%Y")
        self._send_cmd(connection, date_cmd)

        with open(self._cmd_file) as cmd_file:
            for cmd in cmd_file:
                self._send_cmd(connection, cmd)
