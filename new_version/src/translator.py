from src.logger import logger
from src.syntax_analysis.analyzer import SyntaxAnalyzer
from src.lexical_analysis.python import LexicalAnalyzer as LexicalAnalyzerPython
from src.generating.python import Generator as GeneratorPython


class TranslatorError(Exception):
    ...


class Translator:
    def __init__(self):
        self.sa = SyntaxAnalyzer()

        # for Python Dialect
        self.la_python = LexicalAnalyzerPython()
        self.g_python = GeneratorPython()

        self.tokens = []
        self.ast = ''
        self.regex = ''

    def clean_states(self):
        self.tokens = []
        self.ast = ''
        self.regex = ''

    def translate(
            self,
            string,
            input_syntax,
            output_syntax,
    ):

        self.clean_states()

        # lexical analysis phase
        try:
            if input_syntax.lower() == 'python':
                self.tokens = self.la_python(string)
        except Exception as e:
            logger.error(
                message='Error while lexical analysis',
                exc=e,
                raise_exc=TranslatorError
            )

        # syntax analysis phase
        try:
            self.ast = self.sa(self.tokens)
        except Exception as e:
            logger.error(
                message='Error while syntax analysis',
                exc=e,
                raise_exc=TranslatorError
            )

        # generating phase
        try:
            if output_syntax.lower() == 'python':
                self.regex = self.g_python(self.ast)
        except Exception as e:
            logger.error(
                message='Error while generating',
                exc=e,
                raise_exc=TranslatorError
            )
        return self.regex
