from typing import Tuple

import numpy

from src.syntax_analysis.analyzer import SyntaxAnalyzer
from src.lexical_analysis.python import LexicalAnalyzer as LexicalAnalyzerPython
from src.generating.python import Generator as GeneratorPython

__la_python = LexicalAnalyzerPython()
__sa = SyntaxAnalyzer()
__g_python = GeneratorPython()


def is_completely_equal_by_ast(a, b):
    tokens_a = __la_python(a)
    tokens_b = __la_python(b)
    ast_a = __sa(tokens_a)
    ast_b = __sa(tokens_b)
    return ast_a == ast_b


def get_levenshtein_distance(regex_a, regex_b):
    distances = numpy.zeros((len(regex_a) + 1, len(regex_b) + 1))
    for t1 in range(len(regex_a) + 1):
        distances[t1][0] = t1
    for t2 in range(len(regex_b) + 1):
        distances[0][t2] = t2
    for t1 in range(1, len(regex_a) + 1):
        for t2 in range(1, len(regex_b) + 1):
            if regex_a[t1 - 1] == regex_b[t2 - 1]:
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]
                if a <= b and a <= c:
                    distances[t1][t2] = a + 1
                elif b <= a and b <= c:
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1
    return distances[len(regex_a)][len(regex_b)]


def get_ast(regex):
    tokens = __la_python(regex)
    return __sa(tokens)


def get_regex(ast):
    return __g_python(ast)
