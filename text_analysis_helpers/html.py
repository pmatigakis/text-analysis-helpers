import logging
from typing import Optional

import extruct
from articles.extractors import ArticleExtractor
from articles.mss.extractors import MSSArticleExtractor
from bs4 import BeautifulSoup

from text_analysis_helpers.downloaders import download_web_page
from text_analysis_helpers.models import HtmlAnalysisResult, SocialNetworkData
from text_analysis_helpers.processors.html import (
    extract_page_data,
    extract_twitter_card,
)
from text_analysis_helpers.text import TextAnalyser

logger = logging.getLogger(__name__)


class HtmlAnalyser(object):
    """Html content analyser"""

    def __init__(
        self,
        text_analyser: Optional[TextAnalyser] = None,
        article_extractor: Optional[ArticleExtractor] = None,
    ):
        """Create a new HtmlAnalyser

        :param text_analyser: the text analysed to use
        :param article_extractor: the article extractor object that will
            extract the article from the html page
        """
        self.__text_analyser = text_analyser or TextAnalyser()
        self._article_extractor = article_extractor or MSSArticleExtractor()

    def analyse_url(self, url, timeout=5, headers=None, verify=True):
        """Download and analyse the contents of the given url

        :param str url: the url to analyse
        :param int timeout: the request timeout
        :param dict|None headers: the headers to add to the request
        :param boolean verify: verify ssl
        :rtype: HtmlAnalysisResult
        :return: the analysis result
        """
        web_page = download_web_page(
            url=url, timeout=timeout, headers=headers, verify=verify
        )

        return self.analyse(web_page)

    def analyse(self, web_page):
        """Analyse the web page contents

        :param text_analysis_helpers.models.WebPage web_page: the wb page
            contents
        :rtype: HtmlAnalysisResult
        :return: the analysis result
        """
        page_content = self._article_extractor.extract_article(web_page.html)
        text_analysis_result = self.__text_analyser.analyse(page_content)
        soup = BeautifulSoup(web_page.html, "html.parser")
        page_data = extract_page_data(soup)
        extracted_data = extruct.extract(web_page.html, base_url=web_page.url)
        twitter_card = extract_twitter_card(soup)

        return HtmlAnalysisResult(
            url=web_page.url,
            html=web_page.html,
            title=page_data["title"],
            social_network_data=SocialNetworkData(
                opengraph=extracted_data.get("opengraph"), twitter=twitter_card
            ),
            text_data=text_analysis_result,
        )
