from abc import ABC, abstractmethod
from typing import Dict


class KeywordExtractor(ABC):
    """Keyword extractor base"""

    @abstractmethod
    def extract_keywords(self, document: str) -> Dict[str, float]:
        """Extract the keyword from the document

        :param document: the document to process
        :return: returns the extracted keywords
        """
        pass
