import re
from typing import Callable, List

import exrex


def regex_process(string, regex):
    re_comp = re.compile(regex)
    try:
        return re_comp.match(string).group()
    except AttributeError:
        return None


class Utils:
    @staticmethod
    def get_test_strings(
            input_regex: str,
            n_fuzzy_strings: int,
    ):
        return list(
            exrex.generate(
                input_regex,
                limit=n_fuzzy_strings)
        )

    @staticmethod
    def create_training_set(
            test_strings: List,
            original_regex: str,
            process_func: Callable
    ):
        Y = []
        X = []
        for string in test_strings:
            X.append(string)
            Y.append(
                process_func(
                    string=string,
                    regex=original_regex
                )
            )
        return X, Y
