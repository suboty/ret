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
                if case[0] != '1':
                    continue
                _case = case
                _case[1] = ast.literal_eval(_case[1])
                try:
                    generator_output = self.generator(
                        syntax=int(_case[0]),
                        ast=_case[1]
                    )

                except Exception as e:
                    logger.error(
                        message=f'Error while python generating working',
                        exc=GeneratingTestingError,
                    )
                    raise e

                assert generator_output == _case[2], 'Error while testing, ' \
                                                     f'type: <{test_type}>, ' \
                                                     f'case: {_case[1]}, ' \
                                                     f'output: {_case[2]}, ' \
                                                     f'generator output: {generator_output}'
                number_of_processing_cases += 1

        logger.info(f'Test of generating is finish. Number of processing cases: {number_of_processing_cases}')
