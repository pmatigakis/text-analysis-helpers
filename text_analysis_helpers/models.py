import json
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import Dict, Set

from text_analysis_helpers.helpers import current_date

TextStatistics = namedtuple(
    "TextStatistics",
    [
        "sentence_count",
        "word_count",
        "mean_sentence_word_count",
        "median_sentence_word_count",
        "min_sentence_word_count",
        "max_sentence_word_count",
        "average_sentence_word_count",
        "sentence_word_count_std",
        "sentence_word_count_variance",
    ],
)

WebPage = namedtuple("WebPage", ["url", "html"])

SocialNetworkData = namedtuple("SocialNetworkData", ["opengraph", "twitter"])


class BaseAnalysisResult(metaclass=ABCMeta):
    """Base model for all analysis results"""

    def __init__(self):
        creation_date = current_date()

        self.created_at = creation_date.datetime
        self.created_at_timestamp = creation_date.timestamp

    def save(self, output_file: str):
        """Encode to json and save to a file

        :param output_file: the output file
        """
        with open(output_file, "w") as f:
            f.write(self.as_json())

    @abstractmethod
    def as_dict(self) -> dict:
        """Convert the analysis result object into a dictionary

        :return: the result object data as a dictionary
        """
        return {
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S %z"),
            "created_at_timestamp": self.created_at_timestamp,
        }

    def as_json(self) -> str:
        """Convert the analysis result object into a json string

        :return: the data encoded in json
        """
        return json.dumps(self.as_dict())


class TextAnalysisResult(BaseAnalysisResult):
    """Text analysis result"""

    def __init__(
        self,
        text: str,
        keywords: Dict[str, float],
        readability_scores: dict,
        statistics: TextStatistics,
        summary: str,
        named_entities: Dict[str, Set[str]],
    ):
        """Create a new TextAnalysisResult object

        :param text: the text that was analysed
        :param keywords: the extracted keywords
        :param readability_scores: the readability scores
        :param statistics: the text statistics
        :param summary: the text summary
        :param named_entities: the extracted named entities
        """
        super(TextAnalysisResult, self).__init__()

        self.text = text
        self.keywords = keywords
        self.readability_scores = readability_scores
        self.statistics = statistics
        self.summary = summary
        self.named_entities = named_entities

    def as_dict(self):
        data = super(TextAnalysisResult, self).as_dict()

        named_entities = {
            named_entity_type: list(self.named_entities[named_entity_type])
            for named_entity_type in self.named_entities
        }

        data.update(
            {
                "text": self.text,
                "keywords": self.keywords,
                "readability_scores": self.readability_scores,
                "statistics": dict(self.statistics._asdict()),
                "summary": self.summary,
                "named_entities": named_entities,
            }
        )

        return data


class HtmlAnalysisResult(TextAnalysisResult):
    """Html analysis result"""

    def __init__(
        self,
        url: str,
        html: str,
        title: str,
        social_network_data: SocialNetworkData,
        text_data: TextAnalysisResult,
    ):
        """Create a new HtmlAnalysisResult object

        :param url: the web page url
        :param html: the web page content
        :param title: the web page title
        :param social_network_data: the extracted social network data
        :param text_data: the text analysis result for the text that was
            extracted from the web page
        """
        super(HtmlAnalysisResult, self).__init__(
            text=text_data.text,
            keywords=text_data.keywords,
            readability_scores=text_data.readability_scores,
            statistics=text_data.statistics,
            summary=text_data.summary,
            named_entities=text_data.named_entities,
        )

        self.url = url
        self.html = html
        self.title = title
        self.social_network_data = social_network_data

        self._extract_images(social_network_data)
        self._extract_videos(social_network_data)

    def _extract_images(self, social_network_data: SocialNetworkData):
        self.images = []
        twitter_data = social_network_data.twitter or {}

        image = twitter_data.get("image")
        if image:
            self.images.append(image)
        image = twitter_data.get("image:src")
        if image and image not in self.images:
            self.images.append(image)

        for opengraph_item in social_network_data.opengraph or []:
            for property_name, value in opengraph_item.get("properties", []):
                if property_name == "og:image" and value not in self.images:
                    self.images.append(value)

    def _extract_videos(self, social_network_data: SocialNetworkData):
        self.movies = []

        for opengraph_item in social_network_data.opengraph or []:
            for property_name, value in opengraph_item.get("properties", []):
                if property_name == "og:video" and value not in self.movies:
                    self.movies.append(value)

    def as_dict(self):
        data = super(HtmlAnalysisResult, self).as_dict()

        data.update(
            {
                "url": self.url,
                "html": self.html,
                "title": self.title,
                "images": list(self.images),
                "movies": self.movies,
                "social_network_data": {
                    "twitter": self.social_network_data.twitter,
                    "opengraph": self.social_network_data.opengraph,
                },
            }
        )

        return data
