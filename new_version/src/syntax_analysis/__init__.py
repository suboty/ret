from abc import abstractmethod
from enum import Enum
from typing import List


class LexicalAnalyzerBase:
    @abstractmethod
    def __init__(self):
        self.tokens = []

    @abstractmethod
    def __call__(
            self,
            regex: str) -> List:
        pass

    @abstractmethod
    def eat(self, symbol):
        pass
