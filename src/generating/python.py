from typing import Tuple


class Generator:
    def __init__(self):
        self.regex = None

    @staticmethod
    def atom(subtree):
        return subtree[1]

    @staticmethod
    def any():
        return '.'

    def repeat(self, subtree):
        group = self.eat(subtree[1])
        params = subtree[0].split('_')
        if params[2] == 'inf':
            params[2] = ''
        return group + f'{"{"}{params[1]}{","}{params[2]}{"}"}'

    def alt(self, subtree):
        groups = [x[1] for x in subtree[1]]
        regexes = []

        for group in groups:
            _regex = ''
            for subgroup in group:
                _regex += self.eat(subgroup)
            regexes.append(_regex)

        return f'({"|".join(regexes)})'

    @staticmethod
    def escape(subtree):
        return f'\\{subtree[1]}'

    @staticmethod
    def range(subtree):
        params = subtree[0].split('_')
        # TODO: add few ranges and not ranges cases
        return f'[{params[1]}-{params[2]}]'

    def group(self, subtree):
        output = ''
        _alt = False
        for subgroup in subtree[1]:
            if subgroup == 'alt':
                _alt = True
                continue
            if _alt:
                subgroup = ('alt', subgroup)
                _alt = False
            output += self.eat(subgroup)
        return output

    def eat(self, subtree):
        subtree_type = subtree[0]
        if subtree_type == 'atom':
            return self.atom(subtree)
        elif subtree_type == 'any':
            return self.any()
        elif 'repeat' in subtree_type:
            return self.repeat(subtree)
        elif subtree_type == 'alt':
            return self.alt(subtree)
        elif subtree_type == 'escape':
            return self.escape(subtree)
        elif 'range' in subtree_type:
            return self.range(subtree)
        elif subtree_type == 'group':
            return self.group(subtree)
        return ''

    def __call__(self, ast: Tuple, *args, **kwargs):
        self.regex = ''
        # skip "seq" node
        _alt = False
        for subtree in ast[1]:
            if subtree == 'alt':
                _alt = True
                continue
            if _alt:
                subtree = ('alt', subtree)
                _alt = False
            self.regex += self.eat(subtree)
        return self.regex
