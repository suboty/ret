class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if len(self.stack) == 0:
            return None
        removed = self.stack.pop()
        return removed

    def del_by_index(self, index):
        del self.stack[index]

    def get(self):
        return self.stack


class Re2Parsing:
    def __init__(self):
        self.stack = Stack()

    @staticmethod
    def atom(symbol):
        if symbol.isalpha() or symbol.isdigit():
            return 'atom', symbol
        elif symbol == '.':
            return tuple(['any'])

    def __call__(self, expression: str):
        tokens = []

        _current_group = None
        _current_quantifier = None
        _current_left_part = None
        _current_right_part = None

        _state = None
        _cache = None
        _start = None

        for symbol in expression:
            self.stack.push(symbol)
            # print(symbol, tokens, _state, len(self.stack.get()))

            if symbol.isspace():
                continue

            if _current_group is None and _current_quantifier is None and _current_left_part is None:
                _state = 'atom'
                if symbol.isalpha() or symbol.isdigit():
                    tokens.append(('atom', symbol))
                elif symbol == '.':
                    tokens.append(tuple(['any']))
                elif symbol == '(':
                    _current_quantifier = None
                    _current_group = []
                    _cache = []
                    _start = len(self.stack.get()) - 1
                elif symbol == '{':
                    _current_group = None
                    _current_quantifier = []
                    _cache = []
                    _start = len(self.stack.get()) - 1
                elif symbol == '|':
                    _current_quantifier = None
                    _current_left_part = []
                    _current_right_part = []
                    _start = len(self.stack.get()) - 1

                    if self.stack.get()[_start - 1].isalpha() or self.stack.get()[_start - 1].isdigit():
                        _current_left_part = ('atom', self.stack.get()[_start - 1])
                    elif self.stack.get()[_start - 1] == '.':
                        _current_left_part = tuple(['any'])

            elif _current_quantifier is not None:
                _state = 'quantifier'
                if symbol.isalpha() or symbol.isdigit():
                    _cache.append(('atom', symbol))
                elif symbol == '.':
                    _cache.append(tuple(['any']))
                elif symbol == '}':
                    tokens[-1] = ('quantifier', tokens[-1], tuple(_cache))
                    _current_quantifier = None
                    _cache = None
                    _state = 'atom'

            elif _current_group is not None:
                _state = 'group'
                if symbol.isalpha() or symbol.isdigit():
                    _cache.append(('atom', symbol))
                elif symbol == '.':
                    _cache.append(tuple(['any']))
                elif symbol == ')' and _current_left_part is None:
                    tokens.append(('group', tuple(_cache)))
                    _current_group = None
                    _cache = None
                    _state = 'atom'
                elif symbol == ')' and _current_left_part is not None:
                    __left = tuple(_current_left_part) if len(_current_left_part) > 1 else _current_left_part[0]
                    __right = tuple(_cache) if len(_cache) > 1 else _cache[0]
                    tokens.append(('alt', __left, __right))
                    _current_left_part = None
                    _current_group = None
                    _cache = None
                elif symbol == '|':
                    _current_left_part = _cache
                    _cache = []

            elif _current_left_part is not None and _current_group is None:
                _state = 'alt'
                if symbol.isalpha() or symbol.isdigit():
                    _current_right_part = ('atom', symbol)
                elif symbol == '.':
                    _current_right_part = tuple(['any'])
                tokens[-1] = ('alt', _current_left_part, _current_right_part)

        return 'expr', tuple(tokens)


if __name__ == '__main__':
    la = Re2Parsing()

    regexes = [
        'infoTech{0, 5}(bulgaria|2024)',
        'infoTech Conference{0,3}(bulgaria|2024)',
        'infoTech bulgaria)',
        'InfoTech 2024'
    ]

    with open('trees', 'w') as results_file:

        for regex in regexes:
            _ast = la(regex)
            results_file.writelines(str(_ast) + '\n')
