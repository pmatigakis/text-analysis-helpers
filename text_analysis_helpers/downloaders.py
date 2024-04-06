import requests

from text_analysis_helpers.exceptions import WebPageDownloadError
from text_analysis_helpers.models import WebPage


def download_web_page(url: str, timeout: int = 5, **kwargs) -> WebPage:
    """Download a web page

    :param url: the url of the web page
    :param timeout: the request timeout
    :param kwargs: additional arguments to pass to the `requests.get` method
    :return: the web page contents
    """
    response = requests.get(url, timeout=timeout, **kwargs)

    if response.status_code < 200 or response.status_code >= 300:
        raise WebPageDownloadError(
            message="failed to download web page",
            url=url,
            status_code=response.status_code,
            response=response.text,
        )

    return WebPage(url=url, html=response.text)
