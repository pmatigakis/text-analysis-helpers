from collections import namedtuple


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

HtmlAnalysisResult = namedtuple(
    "TextAnalysisResult",
    ["html", "title", "social_network_data", "text_data"]
)
