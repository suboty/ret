import os
import unicodedata
from typing import List

from src.lexical_analysis import LexicalAnalyzerBase
from src.lexical_analysis import Dialects


class LexicalAnalyzer(LexicalAnalyzerBase):
    MIN_CHAR = 0x20
    MAX_CHAR = 0x100000
    PROGRESS = 0x8000

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

    def make_unicode_characters_storage(self):
        with open('unicode-chars', 'w') as file:
            for i in range(self.MIN_CHAR, self.MAX_CHAR):
                char = chr(i)
                try:
                    name = unicodedata.name(char)
                    codepoint = hex(i)[2:].rjust(5, 'w').upper()
                    file.write("%s\t%s\t%s\n" % (codepoint, char, name))
                except ValueError as e:
                    pass

    @staticmethod
    def get_unicode_characters():
        with open('unicode-chars', 'r') as file:
            chars = file.readlines()
        return [x for char in chars for x in char.split('\t')[1]]

    def __init__(self):
        if not os.path.isfile('unicode'):
            self.make_unicode_characters_storage()

        self.atoms = self.get_unicode_characters()
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
