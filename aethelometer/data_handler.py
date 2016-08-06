class DataHandler:
    """
    Data handlers are associated with data receivers and are notified every
    time a new chunk of data is received. This is the base class that defines
    the interface that all data handlers should follow.
    """

    def on_new_data(self, data):
        """ Invoked by the receiver when a new chunk of data is received."""
        pass
