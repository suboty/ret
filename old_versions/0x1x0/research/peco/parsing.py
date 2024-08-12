# Written by https://github.com/worldbeater

from peco import *
from pprint import pprint

expr = lambda s: expr(s)
char = seq(cite(non(one_of('.+*?^$()[]{}|\\'))),
           to(lambda a: ('atom', a)))
interval = seq(char, sym('-'), char,
               to(lambda a, b: ('range', a, b)))

expr = left(alt(
    seq(expr, sym('+'), to(lambda e: ('+', e))),
    seq(expr, sym('*'), to(lambda e: ('*', e))),
    seq(expr, sym('{'), cite(digit), sym('}'),
        to(lambda expr, times: ('repeat', expr, int(times)))),
    seq(sym('['), group(many(alt(interval, char))), sym(']'),
        to(lambda els: ('alt', *els))),
    interval,
    char,
))

regex = seq(group(many(expr)),
            to(lambda e: ('seq', *e)))

state = parse('color: #[0-9A-Fa-f]{6}', regex)
tree = state.stack[-1]


print(tree)
print()
pprint(tree)
