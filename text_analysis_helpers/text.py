from text_analysis_helpers.models import TextAnalysisResult, TextData
from text_analysis_helpers.processors.text import (
    extract_keywords, calculate_readability_scores
)


class TextAnalyser(object):
    def __init__(self, keyword_stop_list=None):
        self.keyword_stop_list = keyword_stop_list

    def analyse(self, text):
        readability_scores = calculate_readability_scores(text)

        keywords = None
        if isinstance(text, str) and len(text) != 0:
            keywords = extract_keywords(
                text=text,
                keyword_stop_list=self.keyword_stop_list
            )

        return TextAnalysisResult(
            text=text,
            text_data=TextData(
                keywords=keywords,
                readability_scores=readability_scores
            )
        )
