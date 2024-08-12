import os
import re
from pathlib import Path

from src.logger import logger

test_data = {}
end_line_regex = re.compile(r'\n$')

test_folders = os.listdir(Path('tests', 'data'))

logger.debug('Start test data loading ...')
for test_folder in os.listdir(Path('tests', 'data')):
    test_data[test_folder] = {}
    for test_type in os.listdir(Path('tests', 'data', test_folder)):
        with open(Path('tests', 'data', test_folder, test_type), 'r') as data_file:
            # TODO: add data auto building
            _data = [
                end_line_regex.sub('', x)
                for x in data_file.readlines()
                if x[:5] != '# ---' and x != '\n'
            ]
            comp_data = []
            _last_input = None
            for i, _ in enumerate(_data):
                if i % 2 == 0:
                    _last_input = _
                else:
                    comp_data.append((_last_input, _))
                    _last_input = None
            test_data[test_folder][test_type] = comp_data
# TODO: add more test data report
logger.debug(f'Test data is loaded. Test types: {list(test_data.keys())}')
