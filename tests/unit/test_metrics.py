import ast

from tests import test_data
from src.logger import logger
from src.metrics.accuracy import get_match_accuracy
from src.metrics.performance import get_performance_metric


class MetricsTestingError(Exception):
    ...


try:
    metrics_test_data = test_data['metrics']
except KeyError:
    logger.error(
        message=f'No test data (no examples in <metrics> folder) for syntax analysis',
        exc=MetricsTestingError,
        raise_exc=KeyError
    )


class TestSyntaxAnalysis:
    def test_cases(self):
        number_of_processing_cases = 0
        for test_type in metrics_test_data.keys():
            logger.info(f'Start test for metrics for cases in <{test_type}> type')
            for case in metrics_test_data[test_type]:
                _inputs = case[0].split(' ')
                _input_syntax = int(_inputs[0])
                _input_regex = str(_inputs[1])
                _input_string = str(_inputs[2])
                _output = int(ast.literal_eval(case[1]))
                if _input_syntax != 1:
                    continue
                try:
                    accuracy = get_match_accuracy(
                        regex=_input_regex,
                        syntax=_input_syntax,
                        phrase=_input_string,
                    )

                except Exception as e:
                    logger.error(
                        message=f'Error while accuracy counting working',
                        exc=MetricsTestingError,
                    )
                    raise e

                try:
                    performance_metric = get_performance_metric(
                        regex=_input_regex,
                        syntax=_input_syntax,
                        n_iter=100
                    )

                    logger.info(f'--- For regex <{_input_regex}> '
                                f'performance metric = <{performance_metric}> sec')
                except Exception as e:
                    logger.error(
                        message=f'Error while performance metric counting working',
                        exc=MetricsTestingError,
                    )
                    raise e

                assert accuracy == _output, 'Error while testing, ' \
                                            f'type: <{test_type}>, ' \
                                            f'case: {_input_regex}, ' \
                                            f'output: {_output}, ' \
                                            f'accuracy: {accuracy}'

                number_of_processing_cases += 1

        logger.info(f'Test of syntax analysis is finish. Number of processing cases: {number_of_processing_cases}')
