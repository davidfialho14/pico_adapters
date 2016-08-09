class AethalometerDecoder:
    """ Implements the decoding of aethalometer data lines. """

    @staticmethod
    def decode(data) -> str:
        """ Aethalometer data lines just need to be converted to strings. """
        return data.decode('utf-8')
