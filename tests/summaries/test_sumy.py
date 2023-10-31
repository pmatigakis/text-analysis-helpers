from unittest import TestCase

from text_analysis_helpers.summaries.sumy import SumySummarizer


class SumySummarizerTests(TestCase):
    def test_summarize(self):
        summarizer = SumySummarizer(sentence_count=2)
        document = """Carl Edward Sagan was an American astronomer and 
        science communicator. His best known scientific contribution is his 
        research on the possibility of extraterrestrial life, including 
        experimental demonstration of the production of amino acids from basic 
        chemicals by radiation. He assembled the first physical messages sent 
        into space, the Pioneer plaque and the Voyager Golden Record, which 
        were universal messages that could potentially be understood by any 
        extraterrestrial intelligence that might find them. He argued in favor 
        of the hypothesis, which has since been accepted, that the high 
        surface temperatures of Venus are the result of the greenhouse 
        effect."""  # noqa
        summary = summarizer.summarize(document)

        self.assertEqual(
            summary,
            "His best known scientific contribution is his research on the "
            "possibility of extraterrestrial life, including experimental "
            "demonstration of the production of amino acids from basic "
            "chemicals by radiation. He argued in favor of the hypothesis, "
            "which has since been accepted, that the high surface "
            "temperatures of Venus are the result of the greenhouse effect.",
        )

    def test_summarize_with_empty_document(self):
        summarizer = SumySummarizer(sentence_count=2)
        summary = summarizer.summarize("")

        self.assertEqual(summary, "")
