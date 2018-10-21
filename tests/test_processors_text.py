from unittest import TestCase, main

from text_analysis_helpers.models import TextStatistics
from text_analysis_helpers.processors.text import calculate_text_statistics


class CalculateTextStatisticsTests(TestCase):
    def test_calculate_text_statistics(self):
        text = "Mary had a little lamb. Whose fleece was white as snow"

        statistics = calculate_text_statistics(text)

        self.assertIsInstance(statistics, TextStatistics)
        self.assertEqual(statistics.sentence_count, 2)
        self.assertEqual(statistics.word_count, 12)


if __name__ == "__main__":
    main()
