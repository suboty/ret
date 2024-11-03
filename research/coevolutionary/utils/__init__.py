import re
from typing import Callable, List, Dict

import exrex


def regex_process(string, regex):
    re_comp = re.compile(regex)
    try:
        return re_comp.match(string).group()
    except AttributeError:
        return None


def parse_history(
        algorithm_history: Dict,
        is_visualize: bool = True
) -> Dict:
    alg_dict = {}

    for i, key in enumerate(algorithm_history.keys()):
        for j, row in enumerate(algorithm_history[key]):
            if j == 0:
                alg_dict[i] = {}
                if is_visualize:
                    alg_dict[i][0] = [row[0]]
                    alg_dict[i][1] = [row[1]]
                    alg_dict[i][2] = [row[2]]
                    alg_dict[i][3] = [row[3]]
                    alg_dict[i][4] = [row[7]]
                    alg_dict[i][5] = [row[6]]
                else:
                    for m in range(8):
                        alg_dict[i][m] = [row[m]]
            else:
                if is_visualize:
                    alg_dict[i][0].append(row[0])
                    alg_dict[i][1].append(row[1])
                    alg_dict[i][2].append(row[2])
                    alg_dict[i][3].append(row[3])
                    alg_dict[i][4].append(row[7])
                    alg_dict[i][5].append(row[6])
                else:
                    for m in range(8):
                        alg_dict[i][m].append(row[m])

    return alg_dict


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
