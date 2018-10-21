import logging

from bs4 import BeautifulSoup

from text_analysis_helpers.downloaders import download_web_page
from text_analysis_helpers.models import HtmlAnalysisResult, SocialNetworkData
from text_analysis_helpers.processors.html import (
    extract_opengraph_data, extract_page_content, extract_page_data,
    extract_twitter_card
)
from text_analysis_helpers.text import TextAnalyser


logger = logging.getLogger(__name__)


class HtmlAnalyser(object):
    def __init__(self, keyword_stop_list=None):
        self.__keyword_stop_list = keyword_stop_list
        self.__text_analyser = TextAnalyser(keyword_stop_list)

    @property
    def keyword_stop_list(self):
        return self.__keyword_stop_list

    @keyword_stop_list.setter
    def keyword_stop_list(self, value):
        self.__keyword_stop_list = value
        self.__text_analyser.keyword_stop_list = value

    def analyse_url(self, url, timeout=5, headers=None, verify=True):
        web_page = download_web_page(
            url=url,
            timeout=timeout,
            headers=headers,
            verify=verify
        )

        return self.analyse(web_page)

    def analyse(self, web_page):
        soup = BeautifulSoup(web_page.html, "html.parser")

        text = extract_page_content(web_page.html)
        text_analysis_result = self.__text_analyser.analyse(text)

        page_data = extract_page_data(soup)
        opengraph_data = extract_opengraph_data(web_page.html)
        twitter_card = extract_twitter_card(soup)

        return HtmlAnalysisResult(
            html=web_page.html,
            title=page_data["title"],
            social_network_data=SocialNetworkData(
                opengraph=opengraph_data,
                twitter=twitter_card
            ),
            text_data=text_analysis_result
        )
