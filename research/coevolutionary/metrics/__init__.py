import time


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
        t0 = time.time() * 1000
        for _ in range(n_iter):
            for test_string in test_strings:
                _ = regex.match(test_string)
        return ((time.time() * 1000 - t0) / n_iter) / len(test_strings)
