import re
import ast


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
