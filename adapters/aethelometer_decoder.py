class AethelometerDecoder:
    """ Implements the decoding of aethelometer data lines. """

    @staticmethod
    def decode(data) -> str:
        """ Aethelometer data lines just need to be converted to strings. """
        return data.decode('utf-8')
