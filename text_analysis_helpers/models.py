from collections import namedtuple
from abc import ABCMeta

from text_analysis_helpers.helpers import render_analysis_result


TextStatistics = namedtuple(
    "TextStatistics",
    ["sentence_count", "word_count", "mean_sentence_word_count",
     "median_sentence_word_count", "min_sentence_word_count",
     "max_sentence_word_count", "average_sentence_word_count",
     "sentence_word_count_std", "sentence_word_count_variance"]
)

WebPage = namedtuple(
    "WebPage",
    ["url", "html", "headers"]
)

SocialNetworkData = namedtuple(
    "SocialNetworkData",
    ["opengraph", "twitter"]
)


class BaseModel(metaclass=ABCMeta):
    DEFAULT_TEMPLATE = None

    def render(self, template=None):
        template = template or self.DEFAULT_TEMPLATE

        return render_analysis_result(self, template)

    def save(self, output_file, template=None):
        content = self.render(template=template)

        with open(output_file, "w") as f:
            f.write(content)


class TextAnalysisResult(BaseModel):
    DEFAULT_TEMPLATE = "text_analysis_result.html"

    def __init__(self, text, keywords, readability_scores, statistics,
                 summary):
        self.text = text
        self.keywords = keywords
        self.readability_scores = readability_scores
        self.statistics = statistics
        self.summary = summary


class HtmlAnalysisResult(BaseModel):
    DEFAULT_TEMPLATE = "html_analysis_result.html"

    def __init__(self, html, title, social_network_data, text_data):
        self.html = html
        self.title = title
        self.social_network_data = social_network_data
        self.text_data = text_data
