import pytest

from pyBLS.v1 import BLSv1Reader
from pyBLS.utils.exceptions import BLSSeriesError


class TestBLSV1(object):

    def setup_class(self):
        self.good_series_1 = ["MPU4900012"]

    def test_invalid_series_name_single(self):

        with pytest.raises(BLSSeriesError):
            BLSv1Reader("BADSERIES").fetch()

    def test_invalid_series_name_batch(self):

        with pytest.raises(BLSSeriesError):
            BLSv1Reader(["MPU4900012", "BADSERIES"]).fetch()

    def test_invalid_date_1(self):
        with pytest.raises(ValueError):
            BLSv1Reader(self.good_series_1, start="BAD").fetch()
