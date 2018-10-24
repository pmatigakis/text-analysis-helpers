from unittest import TestCase, main

from text_analysis_helpers.models import TextAnalysisResult
from text_analysis_helpers.text import TextAnalyser


class TextAnalyserTests(TestCase):
    def test_analyse(self):
        text = """>Lorem ipsum dolor sit amet, consectetur adipiscing elit.
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
        self.assertEqual(len(text_analysis_result.keywords), 20)
        self.assertEqual(
            text_analysis_result.keywords["curabitur justo ante"],
            9.0
        )
        self.assertDictEqual(
            text_analysis_result.readability_scores,
            {
                "automated_readability_index": 8.8,
                "coleman_liau_index": 12.66,
                "dale_chall_readability_score": 10.22,
                "difficult_words": 31,
                "flesch_kincaid_grade": 6.4,
                "flesch_reading_ease": 63.46,
                "gunning_fog": 20.856202531645568,
                "linsear_write_formula": 2.65,
                "smog_index": 9.4,
                "text_standard": '8th and 9th grade'
            }
        )

        statistics = text_analysis_result.statistics
        self.assertEqual(statistics.sentence_count, 10)
        self.assertEqual(statistics.word_count, 96)
        self.assertEqual(statistics.mean_sentence_word_count, 9.6)
        self.assertEqual(statistics.median_sentence_word_count, 10.0)
        self.assertEqual(statistics.min_sentence_word_count, 5)
        self.assertEqual(statistics.max_sentence_word_count, 13)
        self.assertEqual(statistics.average_sentence_word_count, 9.6)
        self.assertAlmostEqual(
            statistics.sentence_word_count_std, 2.33238075793812, 3)
        self.assertAlmostEqual(
            statistics.sentence_word_count_variance, 5.4399999999999995, 3)

        self.assertNotEqual(text_analysis_result.summary, text)

        # TODO: add proper unit tests for the named entities
        self.assertDictEqual(
            text_analysis_result.named_entities,
            {
                'GPE': {
                    'Morbi', 'Pellentesque', 'Duis', 'Nullam', 'Curabitur'},
                'PERSON': {'Quisque'}
            }
        )


if __name__ == "__main__":
    main()
