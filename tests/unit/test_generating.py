import ast

from tests import test_data
from src.logger import logger
from src.generating.python import Generator as PythonGenerator


class GeneratingTestingError(Exception):
    ...


try:
    generator_test_data = test_data['generating']
except KeyError:
    logger.error(
        message=f'No test data (no examples in <generating> folder) for generating',
        exc=GeneratingTestingError,
        raise_exc=KeyError
    )


class TestGenerating:
    generator = PythonGenerator()

    def test_python_cases(self):
        number_of_processing_cases = 0
        for test_type in generator_test_data.keys():
            logger.info(f'Start test for generating for cases in <{test_type}> type')
            for case in generator_test_data[test_type]:
                _inputs = case[0].split(' ')
                _input_syntax = _inputs[0]
                _input_ast = ast.literal_eval(_inputs[1])
                _output = case[1]
                if _input_syntax != '1':
                    continue
                try:
                    generator_output = self.generator(
                        syntax=int(_input_syntax),
                        ast=_input_ast
                    )

                except Exception as e:
                    logger.error(
                        message=f'Error while python generating working',
                        exc=GeneratingTestingError,
                    )
                    raise e

                assert generator_output == _output, 'Error while testing, ' \
                                                    f'type: <{test_type}>, ' \
                                                    f'case: {_input_ast}, ' \
                                                    f'output: {_output}, ' \
                                                    f'generator output: {generator_output}'
                number_of_processing_cases += 1

        logger.info(f'Test of generating is finish. Number of processing cases: {number_of_processing_cases}')
