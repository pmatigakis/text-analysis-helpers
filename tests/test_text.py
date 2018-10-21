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
        self.assertEqual(len(text_analysis_result.text_data.keywords), 20)
        print(text_analysis_result.text_data.keywords)
        self.assertEqual(
            text_analysis_result.text_data.keywords["curabitur justo ante"],
            9.0
        )
        self.assertDictEqual(
            text_analysis_result.text_data.readability_scores,
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
        self.assertEqual(
            text_analysis_result.text_data.statistics.sentence_count, 10)
        self.assertEqual(
            text_analysis_result.text_data.statistics.word_count, 96)


if __name__ == "__main__":
    main()
