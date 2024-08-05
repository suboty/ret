from typing import List

from src.lexical_analysis import LexicalAnalyzerBase
from src.lexical_analysis import Dialects


class LexicalAnalyzer(LexicalAnalyzerBase):

    atoms = list('abcdef0123456789-')

    s2t = {
        # characters
        'alt': '|',
        'any': '.',

        # quantifiers
        '0_or_1': '?',
        '1_or_more': '+',
        '0_or_more': '*',

        # groups
        'start_range': '[',
        'end_range': ']',
        'start_group': '(',
        'end_group': ')',
        'start_quant': '{',
        'end_quant': '}',

        # special
        'escape': '\\'
    }

    f2t = {

    }

    def __init__(self):
        super().__init__()
        self.__dialect_id = Dialects.python.value

    def __call__(
            self,
            regex: str) -> List:
        self.tokens = []
        for symbol in regex:
            self.eat(symbol)
        return self.tokens

    def eat(self, symbol):
        if symbol in self.atoms:
            self.tokens.append(f'{self.__dialect_id}.atom,{symbol}')
        else:
            _find = False
            for key in self.s2t.keys():
                if symbol == self.s2t.get(key):
                    self.tokens.append(f'{self.__dialect_id}.{key}')
