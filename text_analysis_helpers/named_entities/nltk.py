from collections import defaultdict
from typing import Dict, Optional, Set

from nltk import sent_tokenize, word_tokenize
from nltk.data import load as nltk_data_load
from nltk.tag.api import TaggerI
from nltk.tag.perceptron import PerceptronTagger
from nltk.tree import Tree

from text_analysis_helpers.named_entities.extractors import (
    NamedEntityExtractor,
)


class NltkNamedEntityExtractor(NamedEntityExtractor):
    def __init__(self, pos_tagger: Optional[TaggerI] = None, ne_chunker=None):
        self._pos_tagger = pos_tagger or PerceptronTagger()
        self._ne_chunker = ne_chunker or nltk_data_load(
            "chunkers/maxent_ne_chunker/english_ace_multiclass.pickle"
        )

    def extract_named_entities(self, document: str) -> Dict[str, Set[str]]:
        sentences = sent_tokenize(document)
        sentence_words = [word_tokenize(sentence) for sentence in sentences]

        tagged_sentences = [
            self._pos_tagger.tag(sentence) for sentence in sentence_words
        ]
        chunked_sentences = [
            self._ne_chunker.parse(sentence) for sentence in tagged_sentences
        ]

        named_entities = defaultdict(set)
        for sentence in chunked_sentences:
            for item in sentence:
                if isinstance(item, Tree):
                    ne_type = item.label()
                    entity = " ".join(
                        [
                            entity_component[0]
                            for entity_component in item.leaves()
                        ]
                    )

                    named_entities[ne_type].add(entity)

        return dict(named_entities)
