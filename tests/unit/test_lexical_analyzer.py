from tests import test_data

from relt.lexical_analyzer import LexicalAnalyzer


class ErrorTestLexicalAnalyzer(Exception):
    ...


class TestLexicalAnalyzer:
    lexical_analyzer = LexicalAnalyzer()

    def test_lexical_analysis(self):
        for data_ex in test_data:
            if self.lexical_analyzer(data_ex.get('input')) != data_ex.get('tokens'):
                raise ErrorTestLexicalAnalyzer(
                    f"Error while lexical analysis is process! Error expr: <{data_ex.get('input')}>"
                )
