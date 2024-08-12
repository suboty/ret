from relt.lexical_analyzer import LexicalAnalyzer
from relt.syntax_analyzer import SyntaxAnalyzer


class Translator:
    def __init__(self, syntax: str):
        self.lexical_analyzer = LexicalAnalyzer(syntax_name=syntax)
        self.syntax_analyzer = SyntaxAnalyzer()

    def translate(self, expression):
        return self.syntax_analyzer(self.lexical_analyzer(expression))