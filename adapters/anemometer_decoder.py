from data_receiver import InvalidFormatException


class AnemometerDecoder:
    """ Implements the decoding of anemometer data lines. """

    START_BYTE = 0x02
    END_BYTE = b'\x03'

    @staticmethod
    def decode(data: bytes) -> str:
        """
        Anemometer data lines start with an start byte (STX) and end with an
        end byte (ETX) followed by a checksum. The start and end bytes are
        discard as well as the checksum and only the data is returned.
        """

        # ignore if the start bytes is missing
        # start the data after the first comma
        start_index = data.find(b',')
        if start_index == -1:
            raise InvalidFormatException("could not find a comma")

        end_index = data.find(AnemometerDecoder.END_BYTE)

        if end_index == -1:
            raise InvalidFormatException("line is missing the end byte")

        # TODO: perform the checksum
        # for now the checksum is ignored

        # take only the data - remove the end byte and the comma before it
        data = data[start_index + 1:end_index - 1]

        return data.decode('utf-8')
