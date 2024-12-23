import re
import random
from enum import Enum


class ETtoRegexTranslator:
    @staticmethod
    def lexical_analyzer(string):
        sep_symbols = ['(', ')', ',']
        tokens = []
        _current_token = ''
        for symbol in string:
            if symbol in sep_symbols:
                if _current_token != '':
                    tokens.append(_current_token)
                tokens.append(symbol)
                _current_token = ''
            else:
                _current_token += symbol
        return tokens

    @staticmethod
    def generator(tokens, params, terminals, current_state=None):
        result = []
        repeat = False
        for i, token in enumerate(tokens):
            if token in terminals:
                # work with special terminals
                if token == 'escape':
                    result.append('\\')
                elif token == 'any':
                    result.append('.')
                elif token == 'range':
                    result.append(f'[{random.choice(params["range"])}]')
                else:
                    result.append(token)
            # add arguments
            elif token == ',' and current_state == 'alt':
                result.append('|')
            elif token == ')' and repeat is True and current_state is None:
                result.append(f'{"{"}{random.choice(params["repeat"])}{"}"}')
                repeat = False
            elif token == '(' and current_state in ['group', 'alt']:
                result.append(token)
            elif token == ')':
                current_state = None
                result.append(')')
            # check functions
            elif token == 'group':
                current_state = 'group'
            elif token == 'repeat':
                repeat = True
            elif token == 'alt':
                current_state = 'alt'
        return result

    @staticmethod
    def regex_compile(individual, terminals, params):
        individual = re.sub(
            r'\s',
            '',
            str(individual)
        )
        tokens = ETtoRegexTranslator.lexical_analyzer(individual)
        regex = ''.join(
            ETtoRegexTranslator.generator(
                tokens=tokens,
                terminals=terminals,
                params=params,
            )
        )
        try:
            return re.compile(regex), None
        except Exception as e:
            return None, f'error: {e}, string: {regex}'


class NodesTypes(Enum):
    params = -1
    seq = 0
    atom = 1
    any = 2
    repeat = 3
    alt = 4
    altgroup = 5
    group = 6
    range = 7
    escape = 8


class Nodes:
    nodes_types = {}
    max_id = 0

    def __init__(self):
        for node_type in NodesTypes.__members__:
            value = NodesTypes.__members__.get(node_type).value
            self.nodes_types[value] = node_type
            self.max_id = value


class ILtoRegexTranslator:
    def __init__(self, nodes, params):
        self.params = params
        self.nodes = nodes

    def get_regex(self, incidence_list):

        regex = ''

        is_alt = False
        is_group = False
        is_repeat = False

        for incidence in incidence_list:
            if incidence[0] == 0 and is_group:
                regex += ')'
            if incidence[0] == 3:
                continue
            match incidence[1]:
                case -1:
                    continue
                case 0:
                    if incidence[0] == 0:
                        continue
                case 2:
                    regex += '.'
                case 3:
                    if not is_repeat:
                        is_repeat = True
                    continue
                case 5:
                    if is_alt:
                        regex += '|'
                        is_alt = False
                    else:
                        is_alt = True
                case 6:
                    regex += '('
                    is_group = True
                case 7:
                    _params = self.params.get('range')[0]
                    regex += f'[{_params}]'
                case 8:
                    regex += '\\'
                case _:
                    if incidence[0] in [1, 8]:
                        regex += self.nodes[incidence[1]]
            if is_repeat:
                _params = self.params.get('repeat')[0]
                regex += '{' + f'{_params}' + '}'
                is_repeat = False
        return regex

    def regex_compile(self, individual, is_need_string: bool = False):
        try:
            res = [self.get_regex(individual), None]
            res[0] = res[0].replace('alt', '').replace('atom', '')
            if is_need_string:
                return res
            else:
                try:
                    regex = re.compile(res[0])
                    return regex, res[1]
                except Exception as e:
                    raise e
        except Exception as e:
            return None, e
