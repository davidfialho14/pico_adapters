from contextlib import suppress

from connection_handler import ConnectionHandler


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
        # before sending commands always open the file to ensure it exists
        # before sending commands

        with suppress(FileNotFoundError):
            with open(self._cmd_file) as cmd_file:
                # enter in command mode
                self._deploy_cmd(data_receiver, connection, "*")

                # execute commands
                for cmd in cmd_file:
                    cmd = cmd.replace("\n", "")  # clear the \n from the cmd
                    self._deploy_cmd(data_receiver, connection, cmd)

                # close command mode
                self._deploy_cmd(data_receiver, connection, "Q")

