import re


def get_match_accuracy(regex, syntax, phrase):
    if syntax.lower() == 'python':
        reg = re.compile(regex)
        result = reg.match(phrase)
        if result:
            return 1
        return 0
