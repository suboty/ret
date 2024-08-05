import ast

from tests import test_data
from src.logger import logger
from src.syntax_analysis.analyzer import SyntaxAnalyzer


class SyntaxAnalysisTestingError(Exception):
    ...


try:
    sa_test_data = test_data['syntax_analysis']
except KeyError:
    logger.error(
        message=f'No test data (no examples in <syntax_analysis> folder) for syntax analysis',
        exc=SyntaxAnalysisTestingError,
        raise_exc=KeyError
    )


class TestSyntaxAnalysis:
    def test_cases(self):
        number_of_processing_cases = 0
        for test_type in sa_test_data.keys():
            logger.info(f'Start test for syntax analysis for cases in <{test_type}> type')
            for case in sa_test_data[test_type]:
                _case = [ast.literal_eval(x) for x in case]
                try:
                    sa = SyntaxAnalyzer()
                    sa_output = sa(_case[0])

                except Exception as e:
                    logger.error(
                        message=f'Error while python syntax analyzer working',
                        exc=SyntaxAnalysisTestingError,
                    )
                    raise e

                assert sa_output == _case[1], 'Error while testing, ' \
                                              f'type: <{test_type}>, ' \
                                              f'case: {_case[0]}, ' \
                                              f'output: {_case[1]}, ' \
                                              f'sa output: {sa_output}'

                number_of_processing_cases += 1

        logger.info(f'Test of syntax analysis is finish. Number of processing cases: {number_of_processing_cases}')
