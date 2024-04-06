import logging
from typing import Optional

import extruct
from articles.extractors import ArticleExtractor
from articles.mss.extractors import MSSArticleExtractor
from bs4 import BeautifulSoup

from text_analysis_helpers.downloaders import download_web_page
from text_analysis_helpers.exceptions import NoContentError
from text_analysis_helpers.models import (
    HtmlAnalysisResult,
    SocialNetworkData,
    WebPage,
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
        self._text_analyser = text_analyser or TextAnalyser()
        self._article_extractor = article_extractor or MSSArticleExtractor()

    def _extract_page_data(self, soup: BeautifulSoup) -> dict:
        title = soup.find("title")

        return {"title": title.text if title else None}

    def _extract_twitter_card(self, soup: BeautifulSoup) -> dict | None:
        card = {}

        for meta in soup.find_all("meta"):
            name = meta.get("name", "")
            if name.startswith("twitter:"):
                items = name.split(":")
                if len(items) < 2 or (len(items) == 2 and not items[1]):
                    msg = "Invalid twitter card value: twitter_card(%s)"
                    logger.warning(msg, name)
                    continue
                card[":".join(items[1:])] = meta.get("content")

        # if twitter card data could not be extracted then return None instead
        # of an empty dictionary
        if len(card) == 0:
            logger.warning("failed to extract twitter card")
            card = None

        return card

    def analyse_url(
        self,
        url: str,
        timeout: int = 5,
        headers: Optional[dict] = None,
        verify: Optional[bool] = True,
    ) -> HtmlAnalysisResult:
        """Download and analyse the contents of the given url

        :param url: the url to analyse
        :param timeout: the request timeout
        :param headers: the headers to add to the request
        :param verify: verify ssl
        :return: the analysis result
        """
        web_page = download_web_page(
            url=url, timeout=timeout, headers=headers, verify=verify
        )

        return self.analyse(web_page)

    def analyse(self, web_page: WebPage) -> HtmlAnalysisResult:
        """Analyse the web page contents

        :param web_page: the web page contents
        :return: the analysis result
        """
        if len(web_page.html) == 0:
            raise NoContentError()

        page_content = self._article_extractor.extract_article(web_page.html)
        text_analysis_result = self._text_analyser.analyse(page_content)
        soup = BeautifulSoup(web_page.html, "html.parser")
        page_data = self._extract_page_data(soup)
        extracted_data = extruct.extract(web_page.html, base_url=web_page.url)
        twitter_card = self._extract_twitter_card(soup)

        return HtmlAnalysisResult(
            url=web_page.url,
            html=web_page.html,
            title=page_data["title"],
            social_network_data=SocialNetworkData(
                opengraph=extracted_data.get("opengraph"), twitter=twitter_card
            ),
            text_data=text_analysis_result,
        )
