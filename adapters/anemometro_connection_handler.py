import socket
from datetime import datetime

from connection_handler import ConnectionHandler
from logger import Logging


class AnemometerConnectionHandler(ConnectionHandler):
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
        with open(self._cmd_file) as cmd_file:
            # enter in command mode
            self._deploy_cmd(data_receiver, connection, "*")

            # execute commands
            for cmd in cmd_file:
                cmd = cmd.replace("\n", "")  # clear the \n from the cmd
                self._deploy_cmd(data_receiver, connection, cmd)

            # close command mode
            self._deploy_cmd(data_receiver, connection, "Q")

    def _deploy_cmd(self, data_receiver, connection, cmd):
        """
        After sending the command it waits 1 second for answers and
        ignores them.
        """
        # enter in command mode
        self._send_cmd(connection, cmd)
        # expect undefined number of answers
        self._receive_and_log_answer(data_receiver, connection)

    @staticmethod
    def _receive_and_log_answer(data_receiver, connection):
        """
        Waits one second for answers and returns after waiting 1 second
        with no responses. Dumps the answers to the log file with a tag of
        'CONFIGURATION'.
        """
        try:
            while True:
                Logging.info("CONFIGURATION:" +
                             data_receiver.raw_receive(
                                 connection, timeout=1).decode())

        except socket.timeout:
            pass
