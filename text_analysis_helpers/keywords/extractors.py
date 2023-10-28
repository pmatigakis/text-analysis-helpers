from abc import ABC, abstractmethod
from typing import Dict


class KeywordExtractor(ABC):
    @abstractmethod
    def extract_keywords(self, document: str) -> Dict[str, float]:
        pass
