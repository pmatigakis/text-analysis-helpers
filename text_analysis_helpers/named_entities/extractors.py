from abc import ABC, abstractmethod
from typing import Dict, Set


class NamedEntityExtractor(ABC):
    @abstractmethod
    def extract_named_entities(self, document: str) -> Dict[str, Set[str]]:
        pass
