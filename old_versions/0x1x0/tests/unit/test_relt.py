from tests import test_data

from relt.main import Translator


class ErrorTestLexicalAnalyzer(Exception):
    ...


class TestRELT:
    translator = Translator(syntax='python.re')

    def test_relt(self):
        for data_ex in test_data:
            if self.translator.translate(data_ex.get('input')) != data_ex.get('ast'):
                raise ErrorTestLexicalAnalyzer(
                    f"Error while relt process! Error expr: <{data_ex.get('input')}>"
                )
