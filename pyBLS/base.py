import requests
import datetime
import time

try:
    import simplejson as json
except ImportError:
    import json

from pyBLS.utils import _init_session, BLSMessages
from pyBLS.utils.exceptions import (BLSQueryError, BLSAuthError,
                                    BLSSeriesError)


class _BLSBase(object):
    """
    Base class for handling BLS queries

    Attributes
    ----------
    start : string, (defaults to '1/1/2010')
        Starting date, timestamp. Parses many different kind of date
        representations (e.g., 'JAN-01-2010', '1/1/10', 'Jan, 1, 1980')
    end : string, (defaults to today)
        Ending date, timestamp. Same format as starting date.
    retry_count: int, default 3, optional
        Desired number of retries if a request fails
    pause: float, default 0.001, optional
        Pause time between retry attempts
    session: requests_cache.session, default None, optional
        A cached requests-cache session
    api_key : str, optional
        BLS API key. If not provided the environmental variable
        BLS_API_KEY is read. The API key is *required* for version 2.0 use,
        but not for version 1.0.
    """

    # Base URL
    _BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    _BLS_API_HEADERS = {'Content-type': 'application/json'}

    def __init__(self, series=None, start=None, end=None, retry_count=3,
                 pause=0.001, session=None):
        """ Initialize the class

        Parameters
        ----------
        version: int
        api_key: str
        series: str or list
            A valid series ID or list of series IDs
        start: int or str
            A desired start year, defaults to 2015
        end: int or str
            A desired end year for the request, defaults to this year
        retry_count: int
            Desired number of retries if a request fails
        pause: float default 0.001, optional
            Pause time between retry attempts
        session: requests_cache.session, default None, optional
            A cached requests-cache session
        """
        self.series = self._validate_series(series)
        self.start, self.end = self._sanitize_dates(start, end)
        self.retry_count = retry_count
        self.pause = pause
        self.session = _init_session(session)

    @property
    def params(self):
        raise NotImplementedError

    @property
    def limits(self):
        raise NotImplementedError

    @property
    def version(self):
        raise NotImplementedError

    def _validate_response(self, response):
        """ Ensures response from BLS server is valid.

        Parameters
        ----------
        response: requests.response
            A requests.response object

        Returns
        -------
        response: Parsed JSON
            A json-formatted response

        Raises
        ------
        ValueError
            If a single Share symbol is invalid
        BLSQueryError
            If the JSON response is empty or throws an error

        """
        json_response = response.json()
        if "Error Message" in json_response:
            raise BLSQueryError()
        if json_response["status"] == 'REQUEST_NOT_PROCESSED':
            if self.version > 1:
                raise BLSAuthError(self.api_key)
            else:
                raise BLSQueryError()
        elif json_response["status"] == 'REQUEST_SUCCEEDED':
            for message in json_response["message"]:
                if any(code in message for code in
                       BLSMessages.INVALID_SERIES):
                    raise BLSSeriesError(message.split()[-1])

        return json_response

    def _execute_BLS_query(self, data):
        """ Executes HTTP Request
        Given a URL, execute HTTP request from BLS server. If request is
        unsuccessful, attempt is made self.retry_count times with pause of
        self.pause in between.

        Parameters
        ----------
        data: str
            A properly-formatted JSON dump of desired request parameters

        Returns
        -------
        response: requests.response
            Sends requests.response object to validator

        Raises
        ------
        BLSQueryError
            If problems arise when making the query
        """
        pause = self.pause
        for i in range(self.retry_count+1):
            # print(self._BLS_API_URL)
            # print(data)
            # print(self._BLS_API_HEADERS)
            # exit()
            response = self.session.post(url=self._BLS_API_URL, data=data,
                                         headers=self._BLS_API_HEADERS)
            if response.status_code == requests.codes.ok:
                return self._validate_response(response)
            time.sleep(pause)
        raise BLSQueryError()

    def _prepare_query(self):
        """
        Prepares the query
        """
        return json.dumps(self.params)

    def fetch(self):
        """Fetches the latest data
        Prepares the query string based on self.params and executes the
        request

        Returns
        -------
        requests.response
            A resonse object
        """
        data = self._prepare_query()
        return self._execute_BLS_query(data)

    def _validate_series(self, series):
        if isinstance(series, str):
            return [series]
        elif isinstance(series, list):
            if len(series) > self.limits["SERIES_PER_QUERY"]:
                raise ValueError('Invalid year range for version '
                                 '{}'.format(self.version))
            return series
        else:
            raise ValueError("Expected series ID or list of series IDs")

    def _sanitize_dates(self, start, end):
        """
        Return (datetime_start, datetime_end) tuple
        if start is None - default is 2015
        if end is None - default is this year
        """
        if isinstance(start, str):
            start = int(start)
        if isinstance(start, str):
            end = int(end)
        if start is None:
            start = datetime.datetime.now().year - 3
        if end is None:
            end = datetime.datetime.now().year
        if (start) > end:
            raise ValueError('start must be an earlier date than end')
        if end - start > self.limits["YEARS_PER_QUERY"]:
            raise ValueError('Invalid year range for version '
                             '{}'.format(self.version))
        return start, end
