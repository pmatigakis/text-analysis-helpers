from unittest import TestCase, main

from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from tests.keywords.corpora import paper_abstract
from text_analysis_helpers.keywords.rake import Rake


class RakeTests(TestCase):
    def test_extract_keywords(self):
        rake = Rake(
            word_tokenizer=word_tokenize,
            sentence_tokenizer=sent_tokenize,
            stop_words=stopwords.words("english"),
            delimiters=[",", "’", "‘", "“", "”", "“", "?", "—", "."],
        )

        keywords = rake.extract_keywords(paper_abstract)

        expected_keywords_lowercase = {
            "upper bounds": 4.0,
            "algorithms": 1.5,
            "compatibility": 2.0,
            "components": 1.0,
            "considered": 1.5,
            "considered types": 3.166666666666667,
            "constructing": 1.0,
            "construction": 1.0,
            "corresponding algorithms": 3.5,
            "criteria": 2.0,
            "given": 1.0,
            "linear diophantine equations": 8.5,
            "linear constraints": 4.5,
            "minimal generating sets": 8.666666666666666,
            "minimal set": 4.666666666666666,
            "minimal supporting set": 7.666666666666666,
            "mixed types": 3.666666666666667,
            "natural numbers": 4.0,
            "nonstrict inequations": 4.0,
            "set": 2.0,
            "solutions": 3.0,
            "solving": 1.0,
            "strict inequations": 4.0,
            "system": 1.0,
            "systems": 4.0,
            "types": 1.6666666666666667,
            "used": 1.0,
        }

        self.assertCountEqual(
            [keyword.lower() for keyword in keywords.keys()],
            expected_keywords_lowercase.keys(),
        )

        for keyword in keywords:
            self.assertAlmostEqual(
                keywords[keyword],
                expected_keywords_lowercase[keyword.lower()],
                places=3,
            )


if __name__ == "__main__":
    main()
