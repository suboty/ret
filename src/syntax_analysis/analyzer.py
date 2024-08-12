from typing import List, Union, Tuple

from src.logger import logger
from src.syntax_analysis.utils import Stack, Tree
from src.lexical_analysis import Dialects

MAX_LEN = 'inf'


class SyntaxAnalyzer:
    state = None
    current_string = None
    tree: List[Union[List, Tuple, str]] = None
    sub_trees = None
    history = None

    # TODO: add auto mapping for syntax
    escape_mapping = {
        1: {
            # characters
            'alt': '|',
            'any': '.',
            # quantifiers
            '0_or_1': '?',
            '1_or_more': '+',
            '0_or_more': '*',
            # groups
            'start_range': '[',
            'end_range': ']',
            'start_group': '(',
            'end_group': ')',
            'start_quant': '{',
            'end_quant': '}',
        }
    }

    @staticmethod
    def add_root_group(string, is_root_group_needs: bool = False):
        if is_root_group_needs:
            current_dialect = string[0][0]
            return [f"{current_dialect}.start_group"] + string + [f"{current_dialect}.end_group"]
        return string

    @staticmethod
    def remove_root_group(string):
        return 'seq', *string[0][1]

    def start(self, string):
        self.current_string = self.add_root_group(string, is_root_group_needs=True)
        self.state = 'init'
        # TODO: rewrite code for tree as a Stack
        self.tree = []
        self.sub_trees = Stack()
        self.history = 'init'

    def end(self, verbose: bool = False):
        self.state = 'end'
        self.add_step_to_history()
        self.current_string = None
        result = tuple(self.tree)
        if verbose:
            logger.info(result)
            logger.info(self.history)
            logger.info(self.tree)
        result = self.remove_root_group(result)
        logger.info(f'\t\t\t\tReturn: {Tree(result)}')
        return result

    def add_step_to_history(self):
        self.history += f'->{self.state}'

    def tree_append(self, subtree: Tuple):
        if len(self.sub_trees) == 0:
            self.tree.append(subtree)
        else:
            self.sub_trees.get(-1).append(subtree)

    def next_token(self):
        self.add_step_to_history()
        self.current_string = self.current_string[1:]

    def atom(self, token_value: str):
        self.state = 'atom'
        self.tree_append(subtree=('atom', token_value))
        self.next_token()

    def any(self):
        self.state = 'any'
        self.tree_append(subtree=('any',))
        self.next_token()

    def end_group(self):
        self.tree_append(subtree=('end_group',))
        self.next_token()

    def unknown(self):
        self.state = 'unknown'
        self.tree_append(subtree=('--unknown--',))
        self.next_token()

    def quantifier(self, token_meta: Tuple):

        def __get_quantifier_params(token_name):
            params = token_name.split('_or_')
            if params[1] == 'more':
                params[1] = MAX_LEN
            return [int(x) for x in params if x != 'inf']

        self.state = 'quantifier'
        if int(token_meta[0]) in [
            Dialects.python.value
        ]:
            # left associate
            value = self.tree[-1]
            self.tree.pop(-1)
            self.tree_append(subtree=(
                f'repeat_{"_".join([str(x) for x in __get_quantifier_params(token_meta[1])])}',
                value,
            ))
        else:
            # right associate
            # TODO: add for right associate
            pass
        self.next_token()

    def alt(self):
        self.state = 'alt'
        previous_tokens = []
        while self.tree[-1][0] != 'start_group':
            previous_tokens.insert(0, self.tree.pop(-1))
        self.next_token()
        __current_tree_len = len(self.tree)
        next_tokens = []
        while True:
            if next_tokens:
                if next_tokens[-1][0] == 'end_group':
                    next_tokens.pop(-1)
                    break
            self.eat()
            next_tokens.append(self.tree.pop(-1))
        self.tree_append(subtree=(
            'alt',
            (tuple(previous_tokens)),
            (tuple(next_tokens))
        ))

    def range(self):
        # TODO: add few ranges processing
        self.state = 'range'
        borders = []
        while self.get_token_meta()[1] != 'end_range':
            current_token = self.get_token_meta()
            if borders and current_token[2] == '-':
                self.next_token()
                continue
            try:
                borders.append(int(current_token[2]))
            except:
                # TODO cases with alphabet range and not range group
                pass
            self.next_token()
        self.next_token()
        if borders:
            # TODO cases with alphabet range and not range group
            self.tree_append(subtree=(
                'range',
                borders[0],
                borders[1]
            ))

    def escape(self):
        self.state = 'escape'
        self.next_token()
        current_token = self.get_token_meta()
        self.tree_append(subtree=('escape', (
            'atom',
            self.escape_mapping.get(int(current_token[0])).get(current_token[1])
        )))
        self.next_token()

    def group(self):
        self.state = 'group'
        __current_tree_len = len(self.tree)
        self.tree_append(subtree=('start_group',))
        self.next_token()
        token_meta = self.get_token_meta()
        if token_meta and self.current_string:
            while token_meta[1] != 'end_group':
                self.eat()
                token_meta = self.get_token_meta()
                if token_meta is None:
                    break
            self.next_token()
            subtree = []
            for i in range(len(self.tree) - __current_tree_len):
                subtree.insert(0, self.tree.pop(-1))
            subtree = subtree[1:]
            self.tree_append(subtree=(
                'group',
                tuple(subtree)
            ))

    def get_token_meta(self):
        if self.current_string:
            _ = self.current_string[0]
            try:
                token, value = _.split(',', 1)
            except ValueError:
                token = _
                value = None
            token_id, token_name = token.split('.', 1)
            return token_id, token_name, value

    def eat(self):
        # TODO: fix exit from loop
        token_meta = self.get_token_meta()
        logger.info('--------')
        logger.info(self.state)
        logger.info(self.tree)
        logger.info(self.current_string)
        logger.info(token_meta)
        if token_meta is not None:
            if token_meta[1] == 'atom':
                self.atom(token_value=token_meta[2])
            elif token_meta[1] in ('0_or_1', '1_or_more', '0_or_more'):
                self.quantifier(token_meta=token_meta)
            elif token_meta[1] == 'any':
                self.any()
            elif token_meta[1] == 'alt':
                self.alt()
            elif token_meta[1] == 'start_range':
                self.range()
            elif token_meta[1] == 'escape':
                self.escape()
            elif token_meta[1] == 'start_group':
                self.group()
            elif token_meta[1] == 'end_group':
                self.end_group()
            else:
                self.unknown()
        else:
            return 0

    def __call__(self, string: List, *args, **kwargs):
        logger.info(f'\n\t\t\t\tGet: {string}')
        self.start(string)
        while self.current_string:
            self.eat()
        return self.end(verbose=False)
