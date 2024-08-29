import copy
import re
from ast import literal_eval

from src.logger import logger
from src.generating import NodesTypes


class Nodes:
    nodes_types = {}
    max_id = 0

    def __init__(self):
        for node_type in NodesTypes.__members__:
            value = NodesTypes.__members__.get(node_type).value
            self.nodes_types[value] = node_type
            self.max_id = value


class MatrixGenerator:
    allowed_matrix_types = [
        'adjacency',
        'incidence_list'
    ]

    # R x R, R = len(node_types)
    _adjacency_base_matrix = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    params_dict = {
        'repeat': [],
        'range': []
    }

    clean_params_reg = re.compile(r'[0-9_]|inf')
    find_params_reg = re.compile(r'([0-9]_([0-9]|inf))')

    ThisNodesTypes = Nodes()

    @staticmethod
    def eat(ast):
        output = []
        for subgroup in ast:
            if isinstance(subgroup, tuple):
                output.append(MatrixGenerator.eat(subgroup))
            elif isinstance(subgroup, str):
                output.append(subgroup)
        return output

    @staticmethod
    def get_incidence_list_by_nodes(nodes, root_node=None):
        output_lists = []
        root_node = root_node
        for subgroup in nodes:
            if isinstance(subgroup, list):
                output_lists += MatrixGenerator.get_incidence_list_by_nodes(
                    subgroup, root_node
                )
            elif isinstance(subgroup, str):
                if root_node:
                    if subgroup not in MatrixGenerator.ThisNodesTypes.nodes_types.values():
                        if root_node in ['atom', 'escape']:
                            MatrixGenerator.ThisNodesTypes.max_id += 1
                            this_id = MatrixGenerator.ThisNodesTypes.max_id
                            MatrixGenerator.ThisNodesTypes.nodes_types[this_id] = subgroup
                        elif 'repeat' in root_node or 'range' in root_node:
                            MatrixGenerator.params_dict[root_node].append(subgroup)
                    incidence = (
                        MatrixGenerator.get_node_id(root_node),
                        MatrixGenerator.get_node_id(subgroup)
                    )
                    output_lists.append(incidence)
                root_node = subgroup
        return output_lists

    @staticmethod
    def get_node_id(node_name):
        try:
            if 'repeat' in node_name:
                MatrixGenerator.params_dict['repeat'].append(
                    tuple(MatrixGenerator.find_params_reg.findall(node_name)[0][0].split('_'))
                )
            elif 'range' in node_name:
                MatrixGenerator.params_dict['range'].append(
                    tuple(MatrixGenerator.find_params_reg.findall(node_name)[0][0].split('_'))
                )
        except:
            pass
        node_name = MatrixGenerator.clean_params_reg.sub('', node_name)
        try:
            for key in MatrixGenerator.ThisNodesTypes.nodes_types.keys():
                if MatrixGenerator.ThisNodesTypes.nodes_types[key] == node_name:
                    return key
        except Exception as e:
            raise AttributeError(f'Error with {node_name} node. Error: {e}')

    @staticmethod
    def get_adjacency_matrix(ast, base_matrix):
        MatrixGenerator.params_dict = {
            'repeat': [],
            'range': []
        }
        matrix = copy.deepcopy(base_matrix)
        incidence_lists = MatrixGenerator.get_incidence_lists(ast)
        for x, y in incidence_lists:
            if y >= len(matrix):
                continue
            matrix[x][y] = 1
        return matrix

    @staticmethod
    def get_incidence_lists(ast):
        MatrixGenerator.params_dict = {
            'repeat': [],
            'range': []
        }
        nodes = MatrixGenerator.eat(ast)
        incidence_lists = MatrixGenerator.get_incidence_list_by_nodes(nodes)
        return incidence_lists

    def preprocess_params_dict(self):
        self.params_dict['repeat'] = [
            x for i, x
            in enumerate(self.params_dict['repeat'])
            if i % 2 != 0
        ]

    def __call__(self, ast, matrix_type: str):
        matrix_type = matrix_type.lower()
        matrix_allowed_types = MatrixGenerator.allowed_matrix_types
        if matrix_type not in matrix_allowed_types:
            raise NotImplementedError(f'Matrix type for generating must be in {matrix_allowed_types}')

        if isinstance(ast, str):
            ast = literal_eval(ast)

        res = None
        if matrix_type == 'adjacency':
            res = MatrixGenerator.get_adjacency_matrix(ast, self._adjacency_base_matrix)
        elif matrix_type == 'incidence_list':
            res = MatrixGenerator.get_incidence_lists(ast)

        nodes = MatrixGenerator.ThisNodesTypes

        self.preprocess_params_dict()
        return res, nodes


class GeneratorByIncidence:
    def __init__(self):
        self.params = {}
        self.incidence_list = []
        self.nodes = {}

    @staticmethod
    def preprocess_incidence_list(incidence_list):
        previous_incidence = incidence_list[0]
        new_incidence_list = [previous_incidence[0], previous_incidence[1]]

        for incidence in incidence_list[1:]:
            if incidence[0] == incidence[1] == 0:
                new_incidence_list.append(-1)
                continue
            if previous_incidence[1] == incidence[0]:
                new_incidence_list.append(incidence[1])
                previous_incidence = incidence
                continue
            else:
                new_incidence_list.append(incidence[0])
                new_incidence_list.append(incidence[1])
                previous_incidence = incidence

        return new_incidence_list

    @staticmethod
    def get_regex(incidence_list, params, nodes):

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
                    _params = params.get('range')[0]
                    if len(params.get('range')) > 1:
                        params['range'] = params['range'][1:]
                    else:
                        params['range'] = []
                    regex += f'[{_params[0]}-{_params[1]}]'
                case 8:
                    regex += '\\'
                case _:
                    if incidence[0] in [1, 8]:
                        regex += nodes[incidence[1]]
            if is_repeat:
                _params = params.get('repeat')[0]
                if len(params.get('repeat')) > 1:
                    params['repeat'] = params['repeat'][1:]
                else:
                    params['repeat'] = []
                regex += f'{"{"}{_params[0]}{","}{_params[1]}{"}"}'
                is_repeat = False
        return regex

    def clean_storages(self):
        self.params = {}
        self.incidence_list = []
        self.nodes = {}

    def __call__(self, incidence_list, params, nodes):
        self.incidence_list = incidence_list
        self.params = copy.deepcopy(params)
        self.nodes = nodes
        self.clean_storages()
        return self.get_regex(incidence_list, params, nodes)
