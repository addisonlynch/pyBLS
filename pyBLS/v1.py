from pyBLS.base import _BLSBase


class BLSv1Reader(_BLSBase):

    @property
    def params(self):
        p = {
            "seriesid": self.series,
            "startyear": str(self.start),
            "endyear": str(self.end)
        }
        return p

    @property
    def limits(self):
        limits = {
            "SERIES_PER_QUERY": 25,
            "YEARS_PER_QUERY": 10
        }
        return limits

    @property
    def version(self):
        return 1.0
