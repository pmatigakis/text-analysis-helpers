from datetime import datetime
from os import path
from unittest import TestCase, main
from unittest.mock import patch

import arrow
from dateutil.tz import tzutc

from text_analysis_helpers.html import HtmlAnalyser
from text_analysis_helpers.models import WebPage


class HtmlAnalyserTests(TestCase):
    @patch("text_analysis_helpers.models.current_date")
    def test_analyse_content(self, current_date_mock):
        current_date_mock.return_value = arrow.get(
            "2018-10-06T12:30:00.000000+00:00"
        )

        tests_dir = path.dirname(path.abspath(__file__))
        page_file = path.join(tests_dir, "data", "page1.html")
        with open(page_file) as f:
            content = f.read()

        web_page = WebPage(url="http://www.example.com", html=content)

        analyser = HtmlAnalyser()
        result = analyser.analyse(web_page)

        self.assertEqual(result.url, "http://www.example.com")
        self.assertEqual(result.html, content)
        self.assertEqual(result.title, "test page 1")
        self.assertTrue(result.text.startswith("Lorem ipsum dolor sit amet"))
        self.assertTrue(result.text.endswith("lectus id ornare."))
        self.assertEqual(len(result.text), 1608)
        self.assertEqual(len(result.keywords), 63)
        self.assertAlmostEqual(
            max(result.keywords.values()), 61.88333333333334, 3
        )
        self.assertAlmostEqual(min(result.keywords.values()), 1.0, 3)
        self.assertAlmostEqual(
            result.keywords["Ut laoreet nisi ligula"], 15.354545454545455, 3
        )
        self.assertDictEqual(
            result.social_network_data.twitter,
            {
                "card": "summary_large_image",
                "creator": "@example",
                "description": "test page 1 twitter description",
                "image:src": "https://example.com/image_2.png",
                "site": "@example_site",
            },
        )
        self.assertEqual(
            result.social_network_data.opengraph,
            [
                {
                    "namespace": {"og": "http://ogp.me/ns#"},
                    "properties": [
                        ("og:description", "test page 1 description"),
                        ("og:type", "article"),
                        ("og:site_name", "test page 1 site"),
                        ("og:title", "test page 1 title"),
                        ("og:url", "https://example.com"),
                        ("og:image", "https://example.com/image_1.png"),
                    ],
                }
            ],
        )
        self.assertDictEqual(
            result.readability_scores,
            {
                "automated_readability_index": 8.7,
                "coleman_liau_index": 12.72,
                "dale_chall_readability_score": 9.24,
                "difficult_words": 81,
                "flesch_kincaid_grade": 6.3,
                "flesch_reading_ease": 63.66,
                "gunning_fog": 18.304489795918368,
                "linsear_write_formula": 2.5,
                "smog_index": 9.3,
                "text_standard": "8th and 9th grade",
            },
        )

        statistics = result.statistics
        self.assertEqual(statistics.sentence_count, 32)
        self.assertEqual(statistics.word_count, 300)
        self.assertEqual(statistics.mean_sentence_word_count, 9.375)
        self.assertEqual(statistics.median_sentence_word_count, 9.0)
        self.assertEqual(statistics.min_sentence_word_count, 5)
        self.assertEqual(statistics.max_sentence_word_count, 20)
        self.assertEqual(statistics.average_sentence_word_count, 9.375)
        self.assertAlmostEqual(
            statistics.sentence_word_count_std, 3.452806829233283, 3
        )
        self.assertAlmostEqual(
            statistics.sentence_word_count_variance, 11.921875, 3
        )

        self.assertNotEqual(result.summary, result.text)
        self.assertEqual(
            result.images,
            [
                "https://example.com/image_2.png",
                "https://example.com/image_1.png",
            ],
        )
        self.assertEqual(result.movies, [])

        # TODO: add proper unit tests for the named entities
        self.assertDictEqual(
            result.named_entities,
            {
                "GPE": {
                    "Aenean",
                    "Aliquam",
                    "Curabitur",
                    "Donec",
                    "Duis",
                    "Etiam",
                    "Fusce",
                    "Integer",
                    "Lorem",
                    "Maecenas",
                    "Morbi",
                    "Nullam",
                    "Nunc",
                    "Pellentesque",
                    "Quisque",
                    "Sed",
                    "Ut",
                    "Vivamus",
                },
                "PERSON": {"Fusce", "Quisque"},
            },
        )

        self.assertEqual(result.created_at_timestamp, 1538829000)
        self.assertEqual(
            result.created_at, datetime(2018, 10, 6, 12, 30, tzinfo=tzutc())
        )


if __name__ == "__main__":
    main()
