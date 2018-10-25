from collections import namedtuple
from abc import ABCMeta, abstractmethod
import json

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


class BaseAnalysisResult(metaclass=ABCMeta):
    """Base model for all analysis results"""

    DEFAULT_TEMPLATE = None

    def render(self, template=None):
        """Render the analysis result into the given jinja2 template

        If a template is not given then this object will attempt to render the
        analysis result using the default template of the BaseAnalysisResult
        implementation.

        :param str|none template: the path to a jinja2 template
        """
        template = template or self.DEFAULT_TEMPLATE

        return render_analysis_result(self, template)

    def save(self, output_file, template=None):
        """Save the analysis result to a file

        :param str output_file: the out file
        :param str|None template: render the analysis result using this jinja2
            template. If a template is not given then we will use the default
            template for the BaseAnalysisResult implementation
        :return:
        """
        content = self.render(template=template)

        with open(output_file, "w") as f:
            f.write(content)

    @abstractmethod
    def as_dict(self):
        """Convert the analysis result object into a dictionary

        :rtype: dict
        :return: the result object data as a dictionary
        """
        pass

    def as_json(self):
        """Convert the analysis result object into a json string

        :rtype: str
        :return: the data encoded in json
        """
        return json.dumps(self.as_dict())


class TextAnalysisResult(BaseAnalysisResult):
    """Text analysis result"""

    DEFAULT_TEMPLATE = "text_analysis_result.html"

    def __init__(self, text, keywords, readability_scores, statistics,
                 summary, named_entities):
        """Create a new TextAnalysisResult object

        :param str text: the text that was analysed
        :param dict[str, int] keywords: the extracted keywords and their scores
        :param dict[str, T] readability_scores: the readability scores
        :param TextStatistics statistics: the text statistics
        :param str summary: the text summary
        :param dict[str, set[str]] named_entities: the extracted named entities
        """
        self.text = text
        self.keywords = keywords
        self.readability_scores = readability_scores
        self.statistics = statistics
        self.summary = summary
        self.named_entities = named_entities

    def as_dict(self):
        named_entities = {
            named_entity_type: list(self.named_entities[named_entity_type])
            for named_entity_type in self.named_entities
        }

        return {
            "text": self.text,
            "keywords": self.keywords,
            "readability_scores": self.readability_scores,
            "statistics": dict(self.statistics._asdict()),
            "summary": self.summary,
            "named_entities": named_entities

        }


class HtmlAnalysisResult(TextAnalysisResult):
    """Html analysis result"""

    DEFAULT_TEMPLATE = "html_analysis_result.html"

    def __init__(self, html, title, social_network_data, text_data,
                 page_content):
        """Create a new HtmlAnalysisResult object

        :param str html: the web page content
        :param str title: the web page title
        :param SocialNetworkData social_network_data: the extracted social
            network data
        :param TextAnalysisResult text_data: the text analysis result for the
            text that was extracted from the web page
        :param newspaper.Article page_content: the analysed article data
        """
        super(HtmlAnalysisResult, self).__init__(
            text=text_data.text,
            keywords=text_data.keywords,
            readability_scores=text_data.readability_scores,
            statistics=text_data.statistics,
            summary=text_data.summary,
            named_entities=text_data.named_entities
        )

        self.html = html
        self.title = title
        self.social_network_data = social_network_data
        self.top_image = page_content.top_image
        self.images = page_content.imgs
        self.movies = page_content.movies

    def as_dict(self):
        data = super(HtmlAnalysisResult, self).as_dict()

        data["html"] = self.html
        data["title"] = self.title
        data["top_image"] = self.top_image
        data["images"] = list(self.images)
        data["movies"] = self.movies
        data["social_network_data"] = {
            "twitter": self.social_network_data.twitter,
            "opengraph": self.social_network_data.opengraph
        }

        return data
