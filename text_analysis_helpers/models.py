from collections import namedtuple

from text_analysis_helpers.helpers import render_html_analysis_result


TextStatistics = namedtuple(
    "TextStatistics",
    ["sentence_count", "word_count", "mean_sentence_word_count",
     "median_sentence_word_count", "min_sentence_word_count",
     "max_sentence_word_count", "average_sentence_word_count",
     "sentence_word_count_std", "sentence_word_count_variance"]
)

TextAnalysisResult = namedtuple(
    "TextAnalysisResults",
    ["text", "keywords", "readability_scores", "statistics", "summary"]
)

WebPage = namedtuple(
    "WebPage",
    ["url", "html", "headers"]
)

SocialNetworkData = namedtuple(
    "SocialNetworkData",
    ["opengraph", "twitter"]
)


class HtmlAnalysisResult(object):
    def __init__(self, html, title, social_network_data, text_data):
        self.html = html
        self.title = title
        self.social_network_data = social_network_data
        self.text_data = text_data

    def render(self, template="html_analysis_result.html"):
        return render_html_analysis_result(self, template=template)

    def save(self, output_file, template="html_analysis_result.html"):
        content = self.render(template=template)

        with open(output_file, "w") as f:
            f.write(content)
