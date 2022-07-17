from collections import defaultdict
from itertools import combinations_with_replacement


class Rake:
    """RAKE keyword extractor"""

    def __init__(
        self, word_tokenizer, sentence_tokenizer, stop_words, delimiters
    ):
        """Create a new Rake objects

        :param func word_tokenizer: a callable that splits a sentence into a
            list of words
        :param func sentence_tokenizer: a callable tat splits the text into
            sentences
        :param list[str] stop_words: a list of stop words to use
        :param list[str] delimiters: the list of word delimiters
        """
        self._word_tokenizer = word_tokenizer
        self._sentence_tokenizer = sentence_tokenizer
        self._delimiters = delimiters

        self._stop_words = set()
        for stop_word in stop_words:
            self._stop_words.add(stop_word)
            splited_stop_word = word_tokenizer(stop_word)
            self._stop_words.update(splited_stop_word)

    def _extract_candidate_keywords(self, tokenized_document):
        """Extract the candidate keywords from the text

        :param list[list[str]] tokenized_document: the tokenized document
        :rtype: list[list[str]]
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

    def _is_stop_word(self, word):
        """Check if this word is a stop word

        :param str word: the word to check
        :rtype: bool
        :return True if this is a stop word
        """
        return word.lower() in self._stop_words

    def _is_delimiter(self, word):
        """Check if this word is a delimiter

        :param str word: the word to check
        :rtype: bool
        :return True if this word is a delimiter
        """
        return self._is_stop_word(word) or word in self._delimiters

    def _tokenize_document(self, document):
        """Tokenize the given document in a list of tokenized sentences

        :param str document:
        :rtype: list[list[str]]
        :return: return the tokenized document
        """
        tokenized_document = []
        sentences = self._sentence_tokenizer(document)
        for sentence in sentences:
            words = self._word_tokenizer(sentence)
            tokenized_document.append(words)

        return tokenized_document

    def _calculate_word_co_occurrences(self, candidate_keywords):
        """Calculate the word cooccurrences for the candidate keywords

        :param list[list[str]] candidate_keywords: the keywords candidates
        :rtype: dict[str, dict[str, int]]
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

    def _calculate_word_scores(self, word_co_occurrences):
        """Calculate the word score

        :param dict[str, dict[str, int]] word_co_occurrences: the word
            cooccurrences matrix
        :rtype: dict[str, float]
        :return: return a dictionary with the word scores
        """
        word_scores = {}
        for word in word_co_occurrences:
            deg = sum(word_co_occurrences[word].values())
            freq = word_co_occurrences[word][word]
            word_scores[word] = deg / freq

        return word_scores

    def _calculate_candidate_keyword_scores(
        self, candidate_keywords, word_scores
    ):
        """Calculate the candidate keyword scores

        :param list[list[str]] candidate_keywords: the list of candidate
            keywords
        :param dict[str, float] word_scores: the word scores
        :rtype: dict[tuple, float]
        :return: return the candidate keyword scores
        """
        candidate_scores = defaultdict(float)
        for candidate in candidate_keywords:
            for word in candidate:
                candidate_scores[tuple(candidate)] += word_scores[word.lower()]

        return candidate_scores

    def _find_candidate_keyword_aliases(self, candidate_keywords):
        """Find the keyword aliases

        A keyword alias is basically just another form of the keyword that
        contains characters that might differ because they are lowercase or
        uppercase.

        :param list[list[str]] candidate_keywords: the keywords
        :rtype: dict[tuple, list[tuple]]
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
        self, candidate_keyword_aliases, candidate_scores
    ):
        """Calculate the scores of the keyword aliases

        :param dict[tuple, list[tuple]] candidate_keyword_aliases: the keyword
            aliases
        :param dict[tuple float] candidate_scores: the keyword scores
        :rtype: dict[tuple, float]
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

    def extract_keywords(self, document):
        """Extract the keywords from the given document text

        :param document: the document text
        :rtype: list[str]
        :return: a dictionary with the keywords. The key is the keyword and the
            value is the keyword score
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
            " ".join(candicate_keyword): score
            for candicate_keyword, score in candidate_scores.items()
        }
