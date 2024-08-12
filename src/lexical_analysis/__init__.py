from abc import abstractmethod
from enum import Enum
from typing import List

from src.utils import Stack


class LexicalAnalyzerBase:
    @abstractmethod
    def __init__(self):
        self.tokens = []
        self.brackets_stack = Stack()

    @abstractmethod
    def __call__(
            self,
            regex: str) -> List:
        pass

    @abstractmethod
    def eat(self, symbol):
        pass


# TODO: add auto complete for dialects list
class Dialects(Enum):
    python = 1
