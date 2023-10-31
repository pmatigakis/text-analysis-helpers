from typing import Optional


class TextAnalysisHelpersException(Exception):
    """Base text analysis helpers exception"""

    pass


class WebPageDownloadError(TextAnalysisHelpersException):
    """Exception that is raised if there was an error while downloading the
    contents of a web page"""

    def __init__(
        self,
        message: Optional[str] = None,
        url: Optional[str] = None,
        status_code: Optional[int] = None,
        response: Optional[str] = None,
    ):
        """Create a new WebPageDownloadError object

        :param message: the description of the error
        :param url: the url that caused the error to occur
        :param status_code: the response status code
        :param response: the response text
        """
        super(WebPageDownloadError, self).__init__(
            message, url, status_code, response
        )

        self.message = message
        self.url = url
        self.status_code = status_code
        self.response = response
