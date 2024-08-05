import ast

from tests import test_data
from src.logger import logger
from src.lexical_analysis.python import LexicalAnalyzer as LAPython


class LexicalAnalysisTestingError(Exception):
    ...


try:
    la_test_data = test_data['lexical_analysis']
except KeyError:
    logger.error(
        message=f'No test data (no examples in <lexical_analysis> folder) for lexical analysis',
        exc=LexicalAnalysisTestingError,
        raise_exc=KeyError
    )


class TestLexicalAnalysis:

    la_python = LAPython()

    def test_python_cases(self):
        number_of_processing_cases = 0
        for test_type in la_test_data.keys():
            logger.info(f'Start test for lexical analysis for cases in <{test_type}> type')
            for case in la_test_data[test_type]:
                if case[0] != '1':
                    continue
                _case = case
                _case[2] = ast.literal_eval(_case[2])
                try:
                    la_output = self.la_python(
                        regex=_case[1]
                    )

                except Exception as e:
                    logger.error(
                        message=f'Error while python lexical analyzer working',
                        exc=LexicalAnalysisTestingError,
                    )
                    raise e

                assert la_output == _case[2], 'Error while testing, ' \
                                              f'type: <{test_type}>, ' \
                                              f'case: {_case[1]}, ' \
                                              f'output: {_case[2]}, ' \
                                              f'la output: {la_output}'

                number_of_processing_cases += 1

        logger.info(f'Test of lexical analysis is finish. Number of processing cases: {number_of_processing_cases}')
