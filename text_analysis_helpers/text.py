import itertools
from typing import Dict, Optional

import numpy as np
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from textstat.textstat import textstat

from text_analysis_helpers.keywords.extractors import KeywordExtractor
from text_analysis_helpers.keywords.rake import Rake
from text_analysis_helpers.models import TextAnalysisResult, TextStatistics
from text_analysis_helpers.named_entities.extractors import (
    NamedEntityExtractor,
)
from text_analysis_helpers.named_entities.nltk import NltkNamedEntityExtractor
from text_analysis_helpers.summaries.summarizers import Summarizer
from text_analysis_helpers.summaries.sumy import SumySummarizer


class TextAnalyser(object):
    """Text analyser"""

    def __init__(
        self,
        keyword_extractor: Optional[KeywordExtractor] = None,
        summarizer: Optional[Summarizer] = None,
        named_entity_extractor: Optional[NamedEntityExtractor] = None,
    ):
        """Create a new TextAnalyser object

        :param keyword_extractor: the keyword extractor to use
        """
        self.keyword_extractor = keyword_extractor or Rake(
            word_tokenizer=word_tokenize,
            sentence_tokenizer=sent_tokenize,
            stop_words=stopwords.words("english"),
            delimiters=[",", "’", "‘", "“", "”", "“", "?", "—", "."],
        )
        self.summarizer = summarizer or SumySummarizer()
        self.named_entity_extractor = (
            named_entity_extractor or NltkNamedEntityExtractor()
        )

    def analyse_file(self, filename):
        """Analyse the contents of a file

        :param str filename: the path to a file
        :rtype: TextAnalysisResult
        :return: the analysis result
        """
        with open(filename, "r") as f:
            return self.analyse(f.read())

    def _calculate_readability_scores(self, text: str) -> Dict:
        score_functions = [
            "flesch_reading_ease",
            "smog_index",
            "flesch_kincaid_grade",
            "coleman_liau_index",
            "automated_readability_index",
            "dale_chall_readability_score",
            "difficult_words",
            "linsear_write_formula",
            "gunning_fog",
            "text_standard",
        ]

        return {
            score_function: getattr(textstat, score_function)(text)
            for score_function in score_functions
        }

    def _calculate_text_statistics(self, sentences, sentence_words):
        """Calculate the text statistics

        :param list[str] sentences: a list with the text sentences
        :param list[list[str]] sentence_words: a list with the sentences that
            have been tokenized into separate words
        :rtype: TextStatistics
        :return: the calculated text statistics
        """
        words = list(itertools.chain(*sentence_words))

        sentence_word_counts = np.array(
            [len(sentence) for sentence in sentence_words]
        )

        return TextStatistics(
            sentence_count=len(sentences),
            word_count=len(words),
            mean_sentence_word_count=float(sentence_word_counts.mean()),
            median_sentence_word_count=float(np.median(sentence_word_counts)),
            min_sentence_word_count=int(sentence_word_counts.min()),
            max_sentence_word_count=int(sentence_word_counts.max()),
            average_sentence_word_count=float(
                np.average(sentence_word_counts)
            ),
            sentence_word_count_std=float(sentence_word_counts.std()),
            sentence_word_count_variance=float(sentence_word_counts.var()),
        )

    def analyse(self, text):
        """Analyse the given text

        :param str text: the text to analyse
        :rtype: TextAnalysisResult
        :return: the analysis result
        """
        readability_scores = self._calculate_readability_scores(text)

        keywords = None
        if isinstance(text, str) and len(text) != 0:
            keywords = self.keyword_extractor.extract_keywords(text)

        sentences = sent_tokenize(text)
        sentence_words = [word_tokenize(sentence) for sentence in sentences]

        statistics = self._calculate_text_statistics(sentences, sentence_words)
        summary = self.summarizer.summarize(text)
        named_entities = self.named_entity_extractor.extract_named_entities(
            text
        )

        return TextAnalysisResult(
            text=text,
            keywords=keywords,
            readability_scores=readability_scores,
            statistics=statistics,
            summary=summary,
            named_entities=named_entities,
        )
