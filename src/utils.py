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
        try:
            return self.stack[i]
        except IndexError:
            return 0


def get_pretty_ast(ast):
    _atoms = []
    new_ast = []
    for subgroup in ast:
        if isinstance(subgroup, tuple):
            if isinstance(subgroup[0], str) and subgroup[0] == 'atom':
                _atoms.append(subgroup[1])
            else:
                if _atoms:
                    new_ast.append((
                        'atom',
                        ''.join(_atoms)
                    ))
                    _atoms = []
                new_ast.append(get_pretty_ast(subgroup))
        else:
            new_ast.append(subgroup)
    if _atoms:
        new_ast.append((
            'atom',
            ''.join(_atoms)
        ))
        _atoms = []
    return tuple(new_ast)
