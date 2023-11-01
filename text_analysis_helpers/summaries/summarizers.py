from abc import ABC, abstractmethod


class Summarizer(ABC):
    """Base class for all summarizers"""

    @abstractmethod
    def summarize(self, document: str) -> str:
        """Create a summary of the document

        :param document: the document text
        :return: returns the summarized document
        """
        pass
