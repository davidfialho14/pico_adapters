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
