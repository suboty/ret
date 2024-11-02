import re
import statistics
from timeit import Timer
from functools import partial


class Metrics:
    @staticmethod
    def get_match_accuracy(regex, phrase, result):
        try:
            reg_result = regex.match(phrase).group()
            if reg_result == result:
                return 1
            return 0
        except AttributeError:
            return 0

    @staticmethod
    def get_performance_metric(regex, n_iter, test_strings):
        results = []
        for test_string in test_strings:
            timed_run = Timer(partial(regex.match, test_string)).timeit(number=n_iter)
            results.append(timed_run)
        res = statistics.mean(results)
        return res

    @staticmethod
    def get_readability(regex_string):

        result = 0
        reg_for_repeat = re.compile(r'\{.\,.\}|\?')
        reg_for_range = re.compile(r'\[.-.\]')
        reg_for_escape = re.compile(r'\\')
        reg_for_atom = re.compile(r'[a-z]')
        reg_for_any = re.compile(r'\.')
        reg_for_alt = re.compile(r'\|')
        reg_for_group = re.compile(r'\(|\)')

        # look for repeats
        result += 3 * len(reg_for_repeat.findall(regex_string))
        regex_string = reg_for_repeat.sub('', regex_string)

        # look for ranges
        result += 3 * len(reg_for_range.findall(regex_string))
        regex_string = reg_for_range.sub('', regex_string)

        # look for escapes
        result += len(reg_for_escape.findall(regex_string))
        regex_string = reg_for_escape.sub('', regex_string)

        # look for atoms
        result += len(reg_for_atom.findall(regex_string))
        regex_string = reg_for_atom.sub('', regex_string)

        # look for anys
        result += len(reg_for_any.findall(regex_string))
        regex_string = reg_for_any.sub('', regex_string)

        # look for alts
        result += 2 * len(reg_for_alt.findall(regex_string))
        regex_string = reg_for_alt.sub('', regex_string)

        # look for groups
        result += 2 * len(reg_for_group.findall(regex_string))
        regex_string = reg_for_group.sub('', regex_string)

        return result
