class BLSQueryError(Exception):
    """
    This error is thrown when an error occurs with the query to BLS, be it a
    network problem or an invalid query.
    """

    def __str__(self):
        return "An error occurred while making the query."


class BLSAuthError(Exception):
    """
    This error is thrown when an invalid BLS registration key is provided
    """

    def __init__(self, key):
        self.key = key

    def __str__(self):
        return ("The provided key: {} is either invalid or was not authorized "
                "by the BLS server".format(self.key))


class BLSSeriesError(Exception):
    """
    This error is raised when an invalid series is requested
    """

    def __init__(self, series):
        self.series = series

    def __str__(self):
        return("The Series: {} could not be retrieved. Please verify proper "
               "series ID formatting.".format(self.series))
