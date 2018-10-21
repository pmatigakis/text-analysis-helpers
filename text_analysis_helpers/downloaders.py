import requests

from text_analysis_helpers.models import WebPage


def download_web_page(url, timeout=5, headers=None, verify=True):
    response = requests.get(
        url,
        timeout=timeout,
        headers=headers,
        verify=verify
    )

    if response.status_code < 200 or response.status_code >= 300:
        raise ValueError("invalid response status code")

    return WebPage(
        url=url,
        html=response.text,
        headers=dict(response.headers)
    )
