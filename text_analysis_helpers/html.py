import logging

from bs4 import BeautifulSoup

from text_analysis_helpers.processors.text import extract_keywords
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

    def process_content(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")

        text = extract_page_content(html_content)
        page_data = extract_page_data(soup)
        opengraph_data = extract_opengraph_data(html_content)
        twitter_card = extract_twitter_card(soup)

        keywords = None
        if isinstance(text, str) and len(text) != 0:
            keywords = extract_keywords(text)

        return HtmlAnalysisResult(
            web_page_content=WebPageContent(
                html=html_content,
                title=page_data["title"],
                text=text
            ),
            social_network_data=SocialNetworkData(
                opengraph=opengraph_data,
                twitter=twitter_card
            ),
            text_data=TextData(keywords=keywords)
        )
