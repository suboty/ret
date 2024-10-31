import re
import time
import statistics


_performance_schema = 'mean'


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
        if _performance_schema == 'median':
            results = []
            for _ in range(n_iter):
                iter_results = []
                for test_string in test_strings:
                    # nano
                    t0 = time.perf_counter_ns()
                    _ = regex.match(test_string)
                    iter_results.append(time.perf_counter_ns() - t0)
                results.append(statistics.median(iter_results) / len(test_strings))
            return statistics.mean(results)
        else:
            t0 = time.time() * 1000
            for _ in range(n_iter):
                for test_string in test_strings:
                    _ = regex.match(test_string)
            return ((time.time() * 1000 - t0) / n_iter) / len(test_strings)

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
