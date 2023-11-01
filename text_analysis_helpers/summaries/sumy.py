from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.utils import get_stop_words

from text_analysis_helpers.summaries.summarizers import (
    Summarizer as SummarizerBase,
)


class SumySummarizer(SummarizerBase):
    """Summarizer implementation using sumy"""

    def __init__(self, language="english", sentence_count=5):
        """Create a new SumySummarizer object

        :param language: the document language
        :param sentence_count: the number of sentences to return
        """
        self.language = language
        self.sentence_count = sentence_count

    def summarize(self, document: str) -> str:
        parser = PlaintextParser.from_string(
            document, Tokenizer(self.language)
        )
        stemmer = Stemmer(self.language)
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(self.language)

        return " ".join(
            [
                str(sentence)
                for sentence in summarizer(
                    parser.document, self.sentence_count
                )
            ]
        )
