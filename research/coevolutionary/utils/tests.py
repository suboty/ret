from typing import Dict

from scipy.stats import wilcoxon

from coevolutionary.utils import parse_history


def check_wilcoxon(
        history_a: Dict,
        history_b: Dict,
        a_name: str,
        b_name: str,
        a_index: int,
        b_index: int,
        metric_number: int,
        metric_name: str,
        confidence: float = 0.05
):
    a = parse_history(history_a)[a_index][metric_number]
    b = parse_history(history_b)[b_index][metric_number]

    # test works only with same lengths
    if len(a) > len(b):
        a = a[:len(b)]
    else:
        b = b[:len(a)]

    result = wilcoxon(a, b)

    __tick_string = u'\u2713'
    __cross_string = u'\u00D7'

    print(f'The Wilcoxon test for {metric_name} metric')
    if result.pvalue < confidence:
        print(f'{__tick_string} According to the Wilcoxon test {a_name} and {b_name} are different\n')
    else:
        print(f'{__cross_string} According to the Wilcoxon test {a_name} and {b_name} are similar\n')
