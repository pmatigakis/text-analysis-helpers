from unittest import TestCase, main
from unittest.mock import Mock

import arrow

from text_analysis_helpers.models import (
    TextAnalysisResult, TextStatistics, HtmlAnalysisResult, SocialNetworkData
)


class TextAnalysisResultTest(TestCase):
    def setUp(self):
        statistics = TextStatistics(
            sentence_count=10,
            word_count=100,
            mean_sentence_word_count=5.5,
            median_sentence_word_count=6.6,
            min_sentence_word_count=2,
            max_sentence_word_count=12,
            average_sentence_word_count=23.5,
            sentence_word_count_std=0.5,
            sentence_word_count_variance=0.7
        )

        self.analysis_result = TextAnalysisResult(
            text="hello world",
            keywords={
                "keyword_1": 1
            },
            readability_scores={
                "flesch_reading_ease": 1,
                "smog_index": 2,
                "flesch_kincaid_grade": 3,
                "coleman_liau_index": 4,
                "automated_readability_index": 5,
                "dale_chall_readability_score": 6,
                "difficult_words": 7,
                "linsear_write_formula": 8,
                "gunning_fog": 8,
                "text_standard": 10
            },
            statistics=statistics,
            summary="hello",
            named_entities={
                "PERSON": {"john"}
            }
        )

        created_at = arrow.get("2018-10-06 12:30:00 UTC")
        self.analysis_result.created_at = created_at.datetime
        self.analysis_result.created_at_timestamp = created_at.timestamp

    def test_as_dict(self):
        self.assertDictEqual(
            self.analysis_result.as_dict(),
            {
                'keywords': {
                    'keyword_1': 1
                },
                'named_entities': {
                    'PERSON': ['john']
                },
                'readability_scores': {
                    'automated_readability_index': 5,
                    'coleman_liau_index': 4,
                    'dale_chall_readability_score': 6,
                    'difficult_words': 7,
                    'flesch_kincaid_grade': 3,
                    'flesch_reading_ease': 1,
                    'gunning_fog': 8,
                    'linsear_write_formula': 8,
                    'smog_index': 2,
                    'text_standard': 10
                },
                'statistics': {
                    'average_sentence_word_count': 23.5,
                    'max_sentence_word_count': 12,
                    'mean_sentence_word_count': 5.5,
                    'median_sentence_word_count': 6.6,
                    'min_sentence_word_count': 2,
                    'sentence_count': 10,
                    'sentence_word_count_std': 0.5,
                    'sentence_word_count_variance': 0.7,
                    'word_count': 100
                },
                'summary': 'hello',
                'text': 'hello world',
                "created_at": "2018-10-06 12:30:00 +0000",
                "created_at_timestamp": 1538829000,
            }
        )

    def test_as_json(self):
        json_data = self.analysis_result.as_json()

        self.assertIsInstance(json_data, str)
        self.assertTrue(json_data.startswith("{"))
        self.assertTrue(json_data.endswith("}"))


class HtmlAnalysisResultTest(TestCase):
    def setUp(self):
        statistics = TextStatistics(
            sentence_count=10,
            word_count=100,
            mean_sentence_word_count=5.5,
            median_sentence_word_count=6.6,
            min_sentence_word_count=2,
            max_sentence_word_count=12,
            average_sentence_word_count=23.5,
            sentence_word_count_std=0.5,
            sentence_word_count_variance=0.7
        )

        text_data = TextAnalysisResult(
            text="hello world",
            keywords={
                "keyword_1": 1
            },
            readability_scores={
                "flesch_reading_ease": 1,
                "smog_index": 2,
                "flesch_kincaid_grade": 3,
                "coleman_liau_index": 4,
                "automated_readability_index": 5,
                "dale_chall_readability_score": 6,
                "difficult_words": 7,
                "linsear_write_formula": 8,
                "gunning_fog": 8,
                "text_standard": 10
            },
            statistics=statistics,
            summary="hello",
            named_entities={
                "PERSON": {"john"}
            }
        )

        social_netword_data = SocialNetworkData(
            twitter={"twitter_item": "twitter_item_value"},
            opengraph={"opengraph_item": "opengraph_item_value"}
        )

        mock_page_content = Mock()
        mock_page_content.top_image = "http://www.example.com/image.png"
        mock_page_content.imgs = {"http://www.example.com/image.png"}
        mock_page_content.movies = ["http://www.example.com/movie.mp4"]

        self.analysis_result = HtmlAnalysisResult(
            url="http://www.example.com/page_1.html",
            html="some html goes here",
            title="this is the title",
            social_network_data=social_netword_data,
            text_data=text_data,
            page_content=mock_page_content
        )

        created_at = arrow.get("2018-10-06 12:30:00 UTC")
        self.analysis_result.created_at = created_at.datetime
        self.analysis_result.created_at_timestamp = created_at.timestamp

    def test_as_dict(self):
        self.assertDictEqual(
            self.analysis_result.as_dict(),
            {
                "created_at": "2018-10-06 12:30:00 +0000",
                "created_at_timestamp": 1538829000,
                'url': "http://www.example.com/page_1.html",
                'html': 'some html goes here',
                'images': ['http://www.example.com/image.png'],
                'keywords': {
                    'keyword_1': 1
                },
                'movies': ['http://www.example.com/movie.mp4'],
                'named_entities': {
                    'PERSON': ['john']
                },
                'readability_scores': {
                    'automated_readability_index': 5,
                    'coleman_liau_index': 4,
                    'dale_chall_readability_score': 6,
                    'difficult_words': 7,
                    'flesch_kincaid_grade': 3,
                    'flesch_reading_ease': 1,
                    'gunning_fog': 8,
                    'linsear_write_formula': 8,
                    'smog_index': 2,
                    'text_standard': 10
                },
                'social_network_data': {
                    'opengraph': {
                        'opengraph_item': 'opengraph_item_value'
                    },
                    'twitter': {
                        'twitter_item': 'twitter_item_value'
                    }
                },
                'statistics': {
                    'average_sentence_word_count': 23.5,
                    'max_sentence_word_count': 12,
                    'mean_sentence_word_count': 5.5,
                    'median_sentence_word_count': 6.6,
                    'min_sentence_word_count': 2,
                    'sentence_count': 10,
                    'sentence_word_count_std': 0.5,
                    'sentence_word_count_variance': 0.7,
                    'word_count': 100
                },
                'summary': 'hello',
                'text': 'hello world',
                'title': 'this is the title',
                'top_image': 'http://www.example.com/image.png'
            }
        )

    def test_as_json(self):
        json_data = self.analysis_result.as_json()

        self.assertIsInstance(json_data, str)
        self.assertTrue(json_data.startswith("{"))
        self.assertTrue(json_data.endswith("}"))


if __name__ == "__main__":
    main()
