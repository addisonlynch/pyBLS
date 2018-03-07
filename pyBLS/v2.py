import os

from pyBLS.base import _BLSBase


class BLSv2Reader(_BLSBase):

    def __init__(self, series=None, start=None, end=None, catalog=False,
                 calculations=False, annual_average=False, retry_count=3,
                 pause=0.001, session=None, api_key=None):
        super(BLSv2Reader, self).__init__(series=series, start=start, end=end,
                                          retry_count=retry_count,
                                          pause=pause, session=session)
        if api_key is None:
            api_key = os.getenv('BLS_API_KEY')
        if not api_key or not isinstance(api_key, str):
            raise ValueError('The BLS API key must be provided '
                             'either through the api_key variable or '
                             'through the environment varaible '
                             'BLS_API_KEY')
        self.api_key = api_key
        self.catalog = catalog
        self.calculations = calculations
        self.annual_average = annual_average

    @property
    def params(self):
        p = {
            "seriesid": self.series,
            "startyear": str(self.start),
            "endyear": str(self.end),
            "registrationkey": self.api_key
        }
        p.update({"catalog": True} if self.catalog is True else {})
        p.update({"calculations": True} if self.catalog is True else {})
        p.update({"annualaverage": True} if self.catalog is True else {})
        return p

    @property
    def limits(self):
        limits = {
            "SERIES_PER_QUERY": 50,
            "YEARS_PER_QUERY": 20
        }
        return limits

    @property
    def version(self):
        return 2.0
