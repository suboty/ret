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
        return group + f'{"{"}{subtree[2]}{","}{subtree[3]}{"}"}'

    def alt(self, subtree):
        first_group = ''
        second_group = ''
        for subgroup in list(subtree[1]):
            first_group += self.eat(subgroup)
        for subgroup in list(subtree[2]):
            second_group += self.eat(subgroup)

        return f'({first_group}|{second_group})'

    def escape(self, subtree):
        return f'\\{self.eat(subtree[1])}'

    @staticmethod
    def range(subtree):
        # TODO: add few ranges and not ranges cases
        return f'[{subtree[1]}-{subtree[2]}]'

    def group(self, subtree):
        output = ''
        for subgroup in subtree[1]:
            output += self.eat(subgroup)
        return output

    def eat(self, subtree):
        subtree_type = subtree[0]
        if subtree_type == 'atom':
            return self.atom(subtree)
        elif subtree_type == 'any':
            return self.any()
        elif subtree_type == 'repeat':
            return self.repeat(subtree)
        elif subtree_type == 'alt':
            return self.alt(subtree)
        elif subtree_type == 'escape':
            return self.escape(subtree)
        elif subtree_type == 'range':
            return self.range(subtree)
        elif subtree_type == 'group':
            return self.group(subtree)
        return ''

    def __call__(self, ast: Tuple, *args, **kwargs):
        self.regex = ''
        for subtree in ast:
            if subtree == 'seq':
                continue
            self.regex += self.eat(subtree)
        return self.regex
