from collections import defaultdict
from itertools import combinations_with_replacement
from typing import Callable, Dict, List, Optional, Set, Tuple

import nltk
from nltk.corpus import stopwords

from text_analysis_helpers.keywords.extractors import KeywordExtractor


class Rake(KeywordExtractor):
    """RAKE keyword extractor"""

    def __init__(
        self,
        word_tokenizer: Optional[Callable] = None,
        sentence_tokenizer: Optional[Callable] = None,
        stop_words: Optional[List[str]] = None,
        delimiters: Optional[List[str]] = None,
    ):
        """Create a new Rake objects

        :param word_tokenizer: a callable that splits a sentence into a
            list of words
        :param sentence_tokenizer: a callable tat splits the text into
            sentences
        :param stop_words: a list of stop words to use
        :param delimiters: the list of word delimiters
        """
        self._word_tokenizer = word_tokenizer or nltk.word_tokenize
        self._sentence_tokenizer = sentence_tokenizer or nltk.sent_tokenize
        self._delimiters = delimiters or [
            ",",
            "’",
            "‘",
            "“",
            "”",
            "“",
            "?",
            "—",
            ".",
        ]

        self._stop_words = set()
        for stop_word in stop_words or stopwords.words("english"):
            self._stop_words.add(stop_word)
            split_stop_word = self._word_tokenizer(stop_word)
            self._stop_words.update(split_stop_word)

    def _extract_candidate_keywords(
        self, tokenized_document: List[List[str]]
    ) -> List[List[str]]:
        """Extract the candidate keywords from the text

        :param tokenized_document: the tokenized document
        :return: the candidate keywords
        """
        candidate_keywords = []

        for sentence in tokenized_document:
            keyword = []
            for word in sentence:
                if not word:
                    continue

                if self._is_delimiter(word):
                    if keyword:
                        candidate_keywords.append(keyword)
                        keyword = []
                else:
                    keyword.append(word)

            if keyword:
                candidate_keywords.append(keyword)

        return candidate_keywords

    def _is_stop_word(self, word: str) -> bool:
        """Check if this word is a stop word

        :param word: the word to check
        :return True if this is a stop word
        """
        return word.lower() in self._stop_words

    def _is_delimiter(self, word: str) -> bool:
        """Check if this word is a delimiter

        :param word: the word to check
        :return True if this word is a delimiter
        """
        return self._is_stop_word(word) or word in self._delimiters

    def _tokenize_document(self, document: str) -> List[List[str]]:
        """Tokenize the given document in a list of tokenized sentences

        :param document: the document to tokenize
        :return: return the tokenized document
        """
        tokenized_document = []
        sentences = self._sentence_tokenizer(document)
        for sentence in sentences:
            words = self._word_tokenizer(sentence)
            tokenized_document.append(words)

        return tokenized_document

    def _calculate_word_co_occurrences(
        self, candidate_keywords: List[List[str]]
    ) -> Dict[str, Dict[str, int]]:
        """Calculate the word cooccurrences for the candidate keywords

        :param candidate_keywords: the keywords candidates
        :return: return the word cooccurrence matrix
        """
        word_co_occurrences = defaultdict(lambda: defaultdict(int))
        for candidate in candidate_keywords:
            for w1, w2 in combinations_with_replacement(candidate, 2):
                w1 = w1.lower()
                w2 = w2.lower()
                word_co_occurrences[w1][w2] += 1
                if w1 != w2:
                    word_co_occurrences[w2][w1] += 1

        return word_co_occurrences

    def _calculate_word_scores(
        self, word_co_occurrences: Dict[str, Dict[str, int]]
    ) -> Dict[str, float]:
        """Calculate the word score

        :param word_co_occurrences: the word cooccurrences matrix
        :return: return a dictionary with the word scores
        """
        word_scores = {}
        for word in word_co_occurrences:
            deg = sum(word_co_occurrences[word].values())
            freq = word_co_occurrences[word][word]
            word_scores[word] = deg / freq

        return word_scores

    def _calculate_candidate_keyword_scores(
        self,
        candidate_keywords: List[List[str]],
        word_scores: Dict[str, float],
    ) -> Dict[Tuple, float]:
        """Calculate the candidate keyword scores

        :param candidate_keywords: the list of candidate keywords
        :param word_scores: the word scores
        :return: return the candidate keyword scores
        """
        candidate_scores = defaultdict(float)
        for candidate in candidate_keywords:
            for word in candidate:
                candidate_scores[tuple(candidate)] += word_scores[word.lower()]

        return candidate_scores

    def _find_candidate_keyword_aliases(
        self, candidate_keywords: List[List[str]]
    ) -> Dict[Tuple, Set[Tuple]]:
        """Find the keyword aliases

        A keyword alias is basically just another form of the keyword that
        contains characters that might differ because they are lowercase or
        uppercase.

        :param candidate_keywords: the keywords
        :return: a dictionary with the aliases mapping
        """
        candidate_keyword_aliases = defaultdict(set)
        for candidate in candidate_keywords:
            normalised_candidate = tuple([word.lower() for word in candidate])
            candidate_keyword_aliases[normalised_candidate].add(
                tuple(candidate)
            )

        return candidate_keyword_aliases

    def _calculate_candidate_keyword_aliases_scores(
        self,
        candidate_keyword_aliases: Dict[Tuple, Set[Tuple]],
        candidate_scores: Dict[Tuple, float],
    ) -> Dict[Tuple, float]:
        """Calculate the scores of the keyword aliases

        :param candidate_keyword_aliases: the keyword aliases
        :param candidate_scores: the keyword scores
        :return: return the calculated keyword alias scores
        """
        normalized_candidates_scores = defaultdict(float)
        for candidate_keyword_alias in candidate_keyword_aliases.values():
            primary_candidate, *candidate_aliases = candidate_keyword_alias
            normalized_candidates_scores[primary_candidate] = candidate_scores[
                primary_candidate
            ]

            for candidate_alias in candidate_aliases:
                normalized_candidates_scores[
                    primary_candidate
                ] += candidate_scores[candidate_alias]

        return normalized_candidates_scores

    def extract_keywords(self, document: str) -> Dict[str, float]:
        """Extract the keywords from the given document text

        :param document: the document text
        :return: a list with the keywords.
        """
        tokenized_document = self._tokenize_document(document)
        candidate_keywords = self._extract_candidate_keywords(
            tokenized_document
        )
        word_co_occurrences = self._calculate_word_co_occurrences(
            candidate_keywords
        )
        word_scores = self._calculate_word_scores(word_co_occurrences)
        candidate_scores = self._calculate_candidate_keyword_scores(
            candidate_keywords, word_scores
        )
        candidate_keyword_aliases = self._find_candidate_keyword_aliases(
            candidate_keywords
        )
        candidate_scores = self._calculate_candidate_keyword_aliases_scores(
            candidate_keyword_aliases, candidate_scores
        )

        return {
            " ".join(candidate_keyword): score
            for candidate_keyword, score in candidate_scores.items()
        }
