class TextAnalysisHelpersException(Exception):
    pass


class WebPageDownloadError(TextAnalysisHelpersException):
    def __init__(self, message=None, url=None, status_code=None,
                 response=None):
        super(WebPageDownloadError, self).__init__(
            message, url, status_code, response)

        self.message = message
        self.url = url
        self.status_code = status_code
        self.response = response
