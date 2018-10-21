from collections import namedtuple


WebPageContent = namedtuple(
    "WebPageData",
    ["html", "title", "text"]
)

SocialNetworkData = namedtuple(
    "SocialNetworkData",
    ["opengraph", "twitter"]
)

TextData = namedtuple(
    "TextData",
    ["keywords", "readability_scores", "statistics", "summary"]
)

HtmlAnalysisResult = namedtuple(
    "TextAnalysisResult",
    ["web_page_content", "social_network_data", "text_data"]
)

WebPage = namedtuple(
    "WebPage",
    ["url", "html", "headers"]
)


TextAnalysisResult = namedtuple(
    "TextAnalysisResults",
    ["text", "text_data"]
)

TextStatistics = namedtuple(
    "TextStatistics",
    ["sentence_count", "word_count", "mean_sentence_word_count",
     "median_sentence_word_count", "min_sentence_word_count",
     "max_sentence_word_count", "average_sentence_word_count",
     "sentence_word_count_std", "sentence_word_count_variance"]
)
