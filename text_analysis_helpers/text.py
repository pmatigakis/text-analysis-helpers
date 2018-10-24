from text_analysis_helpers.models import TextAnalysisResult
from text_analysis_helpers.processors.text import (
    extract_keywords, calculate_readability_scores, calculate_text_statistics,
    create_summary, extract_named_entities
)


class TextAnalyser(object):
    """Text analyser"""

    def __init__(self, keyword_stop_list=None):
        self.keyword_stop_list = keyword_stop_list

    def analyse_file(self, filename):
        """Analyse the contents of a file

        :param str filename: the path to a file
        :rtype: TextAnalysisResult
        :return: the analysis result
        """
        with open(filename, "r") as f:
            return self.analyse(f.read())

    def analyse(self, text):
        """Analyse the given text

        :param str text: the text to analyse
        :rtype: TextAnalysisResult
        :return: the analysis result
        """
        readability_scores = calculate_readability_scores(text)

        keywords = None
        if isinstance(text, str) and len(text) != 0:
            keywords = extract_keywords(
                text=text,
                keyword_stop_list=self.keyword_stop_list
            )

        statistics = calculate_text_statistics(text)
        summary = create_summary(text)
        named_entities = extract_named_entities(text)

        return TextAnalysisResult(
            text=text,
            keywords=keywords,
            readability_scores=readability_scores,
            statistics=statistics,
            summary=summary,
            named_entities=named_entities
        )
