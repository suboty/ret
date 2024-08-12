import re
import ast

import numpy


class Stack:
    def __init__(self):
        self.stack = []

    def __len__(self):
        return len(self.stack)

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if len(self.stack) == 0:
            return None
        return self.stack.pop()

    def get(self, i):
        return self.stack[i]


class Tree:
    def __init__(self, value, *args):
        self.value = value
        self.children = args
        self.clean_reg = re.compile(r'\-+')

    def __repr__(self, depth=1):
        return_string = [str(self.value)]
        for child in self.children:
            return_string.extend(["\n", "-" * (depth + 1), child.__repr__(depth + 1)])
        return "".join(return_string)

    def get_ind_words(self):
        string = self.__repr__().replace('\n', '')
        return ast.literal_eval('["' + self.clean_reg.sub('", "', string) + '"]')


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
