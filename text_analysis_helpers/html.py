import logging

from bs4 import BeautifulSoup

from text_analysis_helpers.models import HtmlAnalysisResult, SocialNetworkData
from text_analysis_helpers.processors.html import (
    extract_opengraph_data, extract_page_content, extract_page_data,
    extract_twitter_card
)
from text_analysis_helpers.text import TextAnalyser


logger = logging.getLogger(__name__)


class HtmlAnalyser(TextAnalyser):
    def __init__(self, keyword_stop_list=None):
        super(HtmlAnalyser, self).__init__(keyword_stop_list)

    def analyse(self, web_page):
        soup = BeautifulSoup(web_page.html, "html.parser")

        text = extract_page_content(web_page.html)
        text_analysis_result = super(HtmlAnalyser, self).analyse(text)

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
