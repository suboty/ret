import re
import time
import string
import random

ALPHABET = string.digits + string.ascii_letters

TEST_STRING_LENGTH = 100
TEST_STRING = ''.join([
    random.choice(ALPHABET) for _ in range(TEST_STRING_LENGTH)
])


def get_performance_metric(regex, syntax, n_iter):
    # TODO: add syntax ids mapping
    try:
        if syntax == 1:
            reg = re.compile(regex)
        else:
            raise NotImplementedError(f'Syntax {syntax} is not implemented')
    except:
        return None
    t0 = time.time() * 1000
    for _ in range(n_iter):
        _ = reg.match(TEST_STRING)
    return str(
        round(time.time() * 1000 - t0, 5) / n_iter
    )
