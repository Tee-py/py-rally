class RallyAPIError(Exception):
    """Exception raised for Rally GSN Api Errors.

    Attributes:
        status_code -- response status code
        data -- api response data
    """

    def __init__(self, status_code: int, data: str):
        message = f'Rally API Request Error. Status Code: {status_code}; Data: {data}'
        super().__init__(message)


class NetworkClientError(Exception):
    ...
