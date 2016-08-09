import socket

from logger import Logging


class ConnectionHandler:
    """
    Connection handlers are associated with data receivers and are notified
    every time the receiver connects or disconnects with the sender (currently
    disconnection is not supported).
    """

    def on_new_connection(self, data_receiver, connection, sender_address):
        """
        Invoked by the receiver connects with the sender. Takes the address
        of the server in the standard 2-tuple format.
        """
        pass

    def _send_cmd(self, connection, cmd):
        """
        Sends a command in string format to the device.
        Includes the \r\n in the end of the cmd.
        """
        connection.sendall((cmd + "\r\n").encode())

    def _deploy_cmd(self, data_receiver, connection, cmd):
        """
        Sends a command and logs the answers. It waits for an answer 1 second
        """
        # enter in command mode
        self._send_cmd(connection, cmd)

        # expect undefined number of answers
        try:
            while True:
                self._receive_and_log(data_receiver, connection)

        except socket.timeout:
            pass

    def _receive_and_log(self, data_receiver, connection):
        """
        Receives an answer and logs it, before returning, by pre-pending the
        tag 'CONFIGURATION'.
        """
        answer = data_receiver.raw_receive(connection, timeout=1).decode()
        Logging.info("CONFIGURATION:" + answer)
        return answer
