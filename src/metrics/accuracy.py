import re


def get_match_accuracy(regex, syntax, phrase):
    # TODO: add syntax ids mapping
    if syntax == 1:
        reg = re.compile(regex)
        result = reg.match(phrase)
        if result:
            return 1
        return 0
    else:
        raise NotImplementedError(f'Syntax {syntax} is not implemented')
