import os

from .v1 import BLSv1Reader
from .v2 import BLSv2Reader

__author__ = 'Addison Lynch'
__version__ = '0.1.0'


def get_bls_series(series=None, start=None, end=None,
                   catalog=None, calculations=None, annual_average=None,
                   retry_count=3, pause=0.001, session=None, api_key=None):
    if api_key is None and os.getenv("BLS_API_KEY") is None:
        return BLSv1Reader(series=series, start=start, end=end,
                           retry_count=retry_count, pause=pause,
                           session=session)
    else:
        return BLSv2Reader(series=series, start=start, end=end,
                           catalog=catalog, calculations=calculations,
                           annual_average=annual_average,
                           retry_count=retry_count, pause=pause,
                           session=session)
