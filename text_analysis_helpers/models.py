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
    ["keywords", "readability_scores"]
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
