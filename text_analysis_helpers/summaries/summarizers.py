from abc import ABC, abstractmethod


class Summarizer(ABC):
    @abstractmethod
    def summarize(self, document: str) -> str:
        pass
