import re
import argparse

import exrex

import sys
import os

# fix relative paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.metrics.accuracy import get_match_accuracy
from src.metrics.performance import get_performance_metric
from src.metrics.readability import get_readability


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script for counting metrics for input and output regex')
    parser.add_argument('-ir', '--input-regex', type=str, help='Input regex')
    parser.add_argument('-or', '--output-regex', type=str, help='Output regex')
    args = parser.parse_args()

    input_regex = args.input_regex
    output_regex = args.output_regex

    # get tests strings
    test_strings = list(exrex.generate(input_regex))

    # compile input regex
    regex = re.compile(output_regex)

    accuracy_list = []

    for string in test_strings:
        accuracy_list.append(get_match_accuracy(
            regex=regex,
            syntax=1,
            phrase=string
        ))

    res_accuracy = sum(accuracy_list)/len(accuracy_list)

    res_performance = get_performance_metric(
        regex=regex,
        syntax=1,
        n_iter=500
    )

    res_readability = get_readability(
        regex=output_regex,
        syntax=1
    )

    print(f'Input Regex <{input_regex}>'
          f'\nOutput Regex <{output_regex}>'
          f'\nValidate strings len: <{len(test_strings)}>'
          f'\n\thas accuracy <{res_accuracy}>'
          f'\n\tand readability: <{res_readability}>'
          f'\n\tand performance metric <{res_performance}>')
