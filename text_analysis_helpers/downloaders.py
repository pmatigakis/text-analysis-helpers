import requests

from text_analysis_helpers.exceptions import WebPageDownloadError
from text_analysis_helpers.models import WebPage


def download_web_page(url, timeout=5, **kwargs):
    response = requests.get(
        url,
        timeout=timeout,
        **kwargs
    )

    if response.status_code < 200 or response.status_code >= 300:
        raise WebPageDownloadError(
            message="failed to download web page",
            url=url,
            status_code=response.status_code,
            response=response.text
        )

    return WebPage(
        url=url,
        html=response.text,
        headers=dict(response.headers)
    )
