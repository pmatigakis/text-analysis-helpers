from datetime import datetime
from unittest import TestCase, main
from unittest.mock import patch

import arrow
from dateutil.tz import tzutc

from text_analysis_helpers.models import TextAnalysisResult
from text_analysis_helpers.text import TextAnalyser


class TextAnalyserTests(TestCase):
    @patch("text_analysis_helpers.models.current_date")
    def test_analyse(self, current_date_mock):
        current_date_mock.return_value = arrow.get(
            "2018-10-06T12:30:00.000000+00:00"
        )

        text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Morbi ac odio tempus elit imperdiet commodo eu eget libero. Nullam eu ornare
neque, tempus auctor libero. Sed et fermentum magna. Duis id mi vitae mi
vehicula dignissim. Curabitur justo ante, posuere in lobortis ut, tristique ut
metus. Pellentesque placerat est sed est facilisis, vitae rutrum metus commodo.
Quisque sed arcu in nisi auctor pharetra at ut arcu. Pellentesque scelerisque
tincidunt dui sed tincidunt. Duis ut lobortis eros, nec egestas mi."""

        analyser = TextAnalyser()
        text_analysis_result = analyser.analyse(text)

        self.assertIsInstance(text_analysis_result, TextAnalysisResult)
        self.assertEqual(text_analysis_result.text, text)
        self.assertEqual(len(text_analysis_result.keywords), 19)
        self.assertEqual(
            text_analysis_result.keywords["Curabitur justo ante"], 9.0
        )
        self.assertDictEqual(
            text_analysis_result.readability_scores,
            {
                "flesch_reading_ease": 63.46,
                "smog_index": 9.4,
                "flesch_kincaid_grade": 6.4,
                "coleman_liau_index": 10.98,
                "automated_readability_index": 8.3,
                "dale_chall_readability_score": 14.62,
                "difficult_words": 27,
                "linsear_write_formula": 4.15,
                "gunning_fog": 8.22,
                "text_standard": "8th and 9th grade",
            },
        )

        statistics = text_analysis_result.statistics
        self.assertEqual(statistics.sentence_count, 10)
        self.assertEqual(statistics.word_count, 95)
        self.assertEqual(statistics.mean_sentence_word_count, 9.5)
        self.assertEqual(statistics.median_sentence_word_count, 9.5)
        self.assertEqual(statistics.min_sentence_word_count, 5)
        self.assertEqual(statistics.max_sentence_word_count, 13)
        self.assertEqual(statistics.average_sentence_word_count, 9.5)
        self.assertAlmostEqual(
            statistics.sentence_word_count_std, 2.29128784747792, 3
        )
        self.assertAlmostEqual(
            statistics.sentence_word_count_variance, 5.25, 3
        )

        self.assertNotEqual(text_analysis_result.summary, text)

        # TODO: add proper unit tests for the named entities
        self.assertDictEqual(
            text_analysis_result.named_entities,
            {
                "GPE": {
                    "Morbi",
                    "Pellentesque",
                    "Duis",
                    "Nullam",
                    "Lorem",
                    "Curabitur",
                },
                "PERSON": {"Quisque"},
            },
        )

        self.assertEqual(text_analysis_result.created_at_timestamp, 1538829000)
        self.assertEqual(
            text_analysis_result.created_at,
            datetime(2018, 10, 6, 12, 30, tzinfo=tzutc()),
        )


if __name__ == "__main__":
    main()
