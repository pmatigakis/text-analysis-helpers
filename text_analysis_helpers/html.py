import logging

from bs4 import BeautifulSoup

from text_analysis_helpers.processors.text import (
    extract_keywords, calculate_readability_scores
)
from text_analysis_helpers.processors.html import (
    extract_opengraph_data, extract_page_content, extract_page_data,
    extract_twitter_card
)
from text_analysis_helpers.models import (
    HtmlAnalysisResult, WebPageContent, SocialNetworkData, TextData
)


logger = logging.getLogger(__name__)


class HtmlAnalyser(object):
    def __init__(self, keyword_stop_list=None):
        self.keyword_stop_list = keyword_stop_list

    def analyse(self, web_page):
        soup = BeautifulSoup(web_page.html, "html.parser")

        text = extract_page_content(web_page.html)
        readability_scores = calculate_readability_scores(text)
        page_data = extract_page_data(soup)
        opengraph_data = extract_opengraph_data(web_page.html)
        twitter_card = extract_twitter_card(soup)

        keywords = None
        if isinstance(text, str) and len(text) != 0:
            keywords = extract_keywords(
                text=text,
                keyword_stop_list=self.keyword_stop_list
            )

        return HtmlAnalysisResult(
            web_page_content=WebPageContent(
                html=web_page.html,
                title=page_data["title"],
                text=text
            ),
            social_network_data=SocialNetworkData(
                opengraph=opengraph_data,
                twitter=twitter_card
            ),
            text_data=TextData(
                keywords=keywords,
                readability_scores=readability_scores
            )
        )
