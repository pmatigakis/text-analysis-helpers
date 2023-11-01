from abc import ABC, abstractmethod
from typing import Dict, Set


class NamedEntityExtractor(ABC):
    """Named entity extractor base"""

    @abstractmethod
    def extract_named_entities(self, document: str) -> Dict[str, Set[str]]:
        """Extract the named entities from the document

        :param document: the document to process
        :return: returns the extracted named entities
        """
        pass
