from tests import test_data

from relt.syntax_analyzer import SyntaxAnalyzer


class ErrorTestSyntaxAnalyzer(Exception):
    ...


class TestSyntaxAnalyzer:
    syntax_analyzer = SyntaxAnalyzer(syntax='python.re')

    def test_syntax_analysis(self):
        for data_ex in test_data:
            if self.syntax_analyzer(data_ex.get('tokens')) != data_ex.get('ast'):
                raise ErrorTestSyntaxAnalyzer(
                    f"Error while syntax analysis is process! Error expr: <{data_ex.get('input')}>"
                )
