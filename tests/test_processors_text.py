from unittest import TestCase, main

from text_analysis_helpers.models import TextStatistics
from text_analysis_helpers.processors.text import calculate_text_statistics


class CalculateTextStatisticsTests(TestCase):
    def test_calculate_text_statistics(self):
        text = "Mary had a little lamb. Whose fleece was white as snow."

        statistics = calculate_text_statistics(text)

        self.assertIsInstance(statistics, TextStatistics)
        self.assertEqual(statistics.sentence_count, 2)
        self.assertEqual(statistics.word_count, 13)
        self.assertEqual(statistics.mean_sentence_word_count, 6.5)
        self.assertEqual(statistics.median_sentence_word_count, 6.5)
        self.assertEqual(statistics.min_sentence_word_count, 6)
        self.assertEqual(statistics.max_sentence_word_count, 7)
        self.assertEqual(statistics.average_sentence_word_count, 6.5)
        self.assertEqual(statistics.sentence_word_count_std, 0.5)
        self.assertEqual(statistics.sentence_word_count_variance, 0.25)


if __name__ == "__main__":
    main()
