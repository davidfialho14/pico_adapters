import pytest

from anemometer_decoder import AnemometerDecoder
from data_receiver import InvalidFormatException


class TestAnemometerDecoder:
    def test_decode_LineWithSTXAndETX_ReturnsDataInTheMiddleOfSTXAndETX(self):
        fake_data = b'\x02Q,-001.688,+002.459,-001.275,\x0310'

        decoded = AnemometerDecoder.decode(fake_data)

        assert decoded == "Q,-001.688,+002.459,-001.275"

    def test_decode_LineWithMissingSTX_RaisesLoadError(self):
        fake_data = b'Q,-001.688,+002.459,-001.275,\x0310'

        with pytest.raises(InvalidFormatException) as error:
            AnemometerDecoder.decode(fake_data)

        assert str(error.value) == "line is missing the start byte"

    def test_decode_LineWithSTXNotInTheBeginning_RaisesLoadError(self):
        fake_data = b'Q\x02,-001.688,+002.459,-001.275,\x0310'

        with pytest.raises(InvalidFormatException) as error:
            AnemometerDecoder.decode(fake_data)

        assert str(error.value) == "line is missing the start byte"

    def test_decode_LineWithMissingETX_RaisesLoadError(self):
        fake_data = b'\x02Q,-001.688,+002.459,-001.275,10'

        with pytest.raises(InvalidFormatException) as error:
            AnemometerDecoder.decode(fake_data)

        assert str(error.value) == "line is missing the end byte"
